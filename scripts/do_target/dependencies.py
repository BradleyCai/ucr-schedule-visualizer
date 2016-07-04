# Copyright (C) 2015-2016 Ammon Smith and Bradley Cai
# Available for use under the terms of the MIT License.

__all__ = [
    "resolve_full_build_order",
    "resolve_build_order",
    "load_module_recursively",
]

from .static import PROGRAM_NAME
from . import targetobj


def resolve_full_build_order(raw_target_list):
    groups = []

    for name in raw_target_list:
        groups.append(resolve_build_order(name))

    all_targets = []

    for targets in groups:
        if all_targets and all_targets[len(all_targets) - 1] == targets[0]:
            targets.pop(0)

        all_targets += targets

    return all_targets


def resolve_build_order(name):
    has_deps = dict() # { dependency : {who needs it} }
    no_deps = set()
    target_names = set()
    targets = []

    load_module_recursively(name, has_deps, no_deps, target_names)

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
        print(" Targets to order: %s" % target_names)
        print(" has_deps: %s" % has_deps)
        print(" no_deps: %s" % no_deps)
        print(" Resultant order: %s" % targets)
        exit(1)

    return targets


def load_module_recursively(name, has_deps, no_deps, target_names):
    module = targetobj.get_target_module(name)

    # Add it to the dependency graph
    if not module.depends:
        no_deps.add(module)
        target_names.add(name)
    else:
        for depend in set(module.depends):
            if depend in has_deps.keys():
                has_deps[depend].add(module)
                target_names.add(name)
            else:
                has_deps[depend] = {module}
                target_names.add(name)

            if depend not in target_names:
                load_module_recursively(depend, has_deps, no_deps, target_names)

