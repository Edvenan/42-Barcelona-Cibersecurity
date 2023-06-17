from treelib import Tree
from os import walk

try: # python 3+
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


def get_fs_tree(start_path,              # type: str
                include_files=True,      # type: bool
                force_absolute_ids=True  # type: bool
                ):
    """
    Returns a `treelib.Tree` representing the filesystem under `start_path`.
    You can then print the `Tree` object using `tree.show()`
    :param start_path: a string representing an absolute or relative path.
    :param include_files: a boolean (default `True`) indicating whether to also include the files in the tree
    :param force_absolute_ids: a boolean (default `True`) indicating of tree node ids should be absolute. Otherwise they
        will be relative if start_path is relative, and absolute otherwise.
    :return:
    """
    tree = Tree()
    first = True
    for root, _, files in walk(start_path):
        p_root = Path(root)
        if first:
            parent_id = None
            first = False
        else:
            parent = p_root.parent
            parent_id = parent.absolute() if force_absolute_ids else parent

        p_root_id = p_root.absolute() if force_absolute_ids else p_root
        tree.create_node(tag="%s/" % (p_root.name if p_root.name != "" else "."),
                         identifier=p_root_id, parent=parent_id)
        if include_files:
            for f in files:
                f_id = p_root_id / f
                tree.create_node(tag=f_id.name, identifier=f_id, parent=p_root_id)

    return tree