# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

__all__ = [
    "resolve_full_build_order",
    "resolve_build_order",
    "load_module_recursively",
    "print_full_dependency_chain",
]

from .static import PROGRAM_NAME
from .tree import Tree
from . import targetobj


def resolve_full_build_order(raw_target_list, verbose=False, asciionly=False):
    groups = []

    for name in raw_target_list:
        groups.append(resolve_build_order(name, verbose, asciionly))

    all_targets = []

    for targets in groups:
        if all_targets and all_targets[len(all_targets) - 1] == targets[0]:
            targets.pop(0)

        all_targets += targets

    if verbose:
        print("(info) Combined dependency list: %s" % get_dependency_list(all_targets))

    return all_targets


def resolve_build_order(name, verbose=False, asciionly=False):
    has_deps = dict() # { dependency : {who needs it} }
    no_deps = set()
    target_names = set()
    targets = []

    load_module_recursively(name, has_deps, no_deps, target_names, verbose)

    if not no_deps:
        print("%s: Cyclic dependency chain detected." % PROGRAM_NAME)

        if verbose:
            print("(info) Targets to order: %s" % target_names)
            print("(info) has_deps: %s" % get_dependency_dict(has_deps))

        exit(1)

    if verbose:
        print("(info) Full dependency chain:")

    print_full_dependency_chain(name, has_deps, no_deps, asciionly)

    # Resolve dependencies
    while no_deps:
        target = no_deps.pop()
        targets.append(target)

        for node in has_deps.get(target.name, ()):
            node.depends.remove(target.name)
            if not node.depends:
                no_deps.add(node)

    if len(targets) != len(target_names):
        print("%s: No way to satisfy dependencies." % PROGRAM_NAME)

        if verbose:
            print("(info) Targets to order: %s" % target_names)
            print("(info) has_deps: %s" % get_dependency_dict(has_deps))
            print("(info) no_deps: %s" % no_deps)
            print("(info) Resultant order: %s" % targets)
        exit(1)

    if verbose:
        name_list = []

        for target in targets:
            name_list.append(target.name)

        print("(info) Dependency order: %s" % ", ".join(name_list))

    return targets


def load_module_recursively(name, has_deps, no_deps, target_names, verbose=False):
    module = targetobj.get_target_module(name)

    # Add it to the dependency graph
    if not module.depends:
        if verbose:
            print("(info) %s has no dependencies." % name)

        no_deps.add(module)
        target_names.add(name)
    else:
        for depend in set(module.depends):
            if name == depend:
                print("%s cannot depend on itself." % name)
                exit(1)

            if verbose:
                print("(info) %s depends on %s." % (name, depend))

            if depend in has_deps.keys():
                has_deps[depend].add(module)
                target_names.add(name)
            else:
                has_deps[depend] = {module}
                target_names.add(name)

            if depend not in target_names:
                if verbose:
                    print("(info) Adding unloaded dependency %s." % depend)

                load_module_recursively(depend, has_deps, no_deps, target_names)


def get_dependency_list(targets):
    name_list = []

    for target in targets:
        name_list.append(target.name)

    return ", ".join(name_list)


def get_dependency_dict(deps):
    name_dict = {}

    for dep in deps.keys():
        for needed_by in deps[dep]:
            needed_by = needed_by.name
            if needed_by in name_dict.keys():
                name_dict[needed_by].add(dep)
            else:
                name_dict[needed_by] = {dep}

    return name_dict


def get_dependency_subtree(name, dep_dict):
    deps = {}

    for dep in dep_dict.get(name, ()):
        deps[dep] = get_dependency_subtree(dep, dep_dict)

    return deps


def print_full_dependency_chain(name, has_deps, no_deps, asciionly):
    dep_dict = get_dependency_dict(has_deps)
    deps = get_dependency_subtree(name, dep_dict)
    tree = Tree(name, deps)
    tree.display(use_ascii=asciionly, bullet=" * ")

