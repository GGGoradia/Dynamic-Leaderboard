class TreeNode:
    def __init__(self, name, score):
        self.name = name
        self.score = score
        self.left = None
        self.right = None

class Leaderboard:
    def __init__(self):
        self.root = None

    def add_player(self, name, score):
        # Insert new player using BFS into the binary tree
        if self.root is None:
            self.root = TreeNode(name, score)
        else:
            self._bfs_insert(self.root, name, score)

    def _bfs_insert(self, node, name, score):
        queue = [node]
        while queue:
            current = queue.pop(0)
            if current.left is None:
                current.left = TreeNode(name, score)
                return
            else:
                queue.append(current.left)
            if current.right is None:
                current.right = TreeNode(name, score)
                return
            else:
                queue.append(current.right)

    def get_leaderboard(self):
        # Fetch all players in BFS order
        if self.root is None:
            return []
        return self._bfs_traverse(self.root)

    def _bfs_traverse(self, node):
        result = []
        queue = [node]
        while queue:
            current = queue.pop(0)
            result.append({'name': current.name, 'score': current.score})
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return result
