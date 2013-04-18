import unittest
from doku import dlx


class NodeTestCase(unittest.TestCase):

    def test_init_is_referential(self):
        node = dlx.Node()

        assert node.column is node
        assert node.left is node
        assert node.right is node
        assert node.up is node
        assert node.down is node

    def test_init_none_links(self):
        node = dlx.Node(column=None,
                        left=None,
                        right=None,
                        up=None,
                        down=None)

        assert node.column is node
        assert node.left is node
        assert node.right is node
        assert node.up is node
        assert node.down is node

    def test_init_links(self):
        column = dlx.Node()
        left = dlx.Node()
        right = dlx.Node()
        up = dlx.Node()
        down = dlx.Node()

        node = dlx.Node(column=column,
                        left=left,
                        right=right,
                        up=up,
                        down=down)

        assert node.column is column
        assert node.left is left
        assert node.right is right
        assert node.up is up
        assert node.down is down

    def test_add_above(self):
        n1 = dlx.Node()
        n2 = dlx.Node()
        n3 = dlx.Node()
        n1.addAbove(n2)
        n1.addAbove(n3)

        assert n1.up is n3
        assert n1.down is n2
        assert n1.column is n1
        assert n2.up is n1
        assert n2.down is n3
        assert n2.column is n1
        assert n3.up is n2
        assert n3.down is n1
        assert n3.column is n1
        assert not hasattr(n1, 'size')

    def test_add_below(self):
        n1 = dlx.Node()
        n2 = dlx.Node()
        n3 = dlx.Node()
        n1.addBelow(n2)
        n1.addBelow(n3)

        assert n1.up is n2
        assert n1.down is n3
        assert n1.column is n1
        assert n2.up is n3
        assert n2.down is n1
        assert n2.column is n1
        assert n3.up is n1
        assert n3.down is n2
        assert n3.column is n1
        assert not hasattr(n1, 'size')

    def test_add_left(self):
        n1 = dlx.Node()
        n2 = dlx.Node()
        n3 = dlx.Node()
        n1.addLeft(n2)
        n1.addLeft(n3)

        assert n1.left is n3
        assert n1.right is n2
        assert n1.column is n1
        assert n2.left is n1
        assert n2.right is n3
        assert n2.column is n2
        assert n3.left is n2
        assert n3.right is n1
        assert n3.column is n3

    def test_add_right(self):
        n1 = dlx.Node()
        n2 = dlx.Node()
        n3 = dlx.Node()
        n1.addRight(n2)
        n1.addRight(n3)

        assert n1.left is n2
        assert n1.right is n3
        assert n1.column is n1
        assert n2.left is n3
        assert n2.right is n1
        assert n2.column is n2
        assert n3.left is n1
        assert n3.right is n2
        assert n3.column is n3

    def test_irow_single(self):
        n1 = dlx.Node()
        assert hasattr(n1.irow, '__iter__')
        assert len(list(n1.irow)) == 0

    def test_irow_many(self):
        n1 = dlx.Node()
        n2 = dlx.Node()
        n3 = dlx.Node()
        n4 = dlx.Node()
        n1.addRight(n2)
        n2.addRight(n3)
        n3.addRight(n4)

        self.assertEqual(list(n1.irow), [n2, n3, n4])
        self.assertEqual(list(n2.irow), [n3, n4, n1])
        self.assertEqual(list(n3.irow), [n4, n1, n2])
        self.assertEqual(list(n4.irow), [n1, n2, n3])

    def test_iter_many(self):
        n1 = dlx.Node()
        n2 = dlx.Node()
        n3 = dlx.Node()
        n4 = dlx.Node()
        n1.addRight(n2)
        n2.addRight(n3)
        n3.addRight(n4)

        self.assertEqual(list(n1), [n2, n3, n4])
        self.assertEqual(list(n2), [n3, n4, n1])
        self.assertEqual(list(n3), [n4, n1, n2])
        self.assertEqual(list(n4), [n1, n2, n3])

    def test_icolumn_single(self):
        n1 = dlx.Node()
        assert hasattr(n1.icolumn, '__iter__')
        assert len(list(n1.icolumn)) == 0

    def test_icolumn_many(self):
        n1 = dlx.Node()
        n2 = dlx.Node()
        n3 = dlx.Node()
        n4 = dlx.Node()
        n1.addBelow(n2)
        n2.addBelow(n3)
        n3.addBelow(n4)

        self.assertEqual(list(n1.icolumn), [n2, n3, n4])
        self.assertEqual(list(n2.icolumn), [n3, n4, n1])
        self.assertEqual(list(n3.icolumn), [n4, n1, n2])
        self.assertEqual(list(n4.icolumn), [n1, n2, n3])

    def test_detach_self(self):
        n1 = dlx.Node()
        n1.detach()

        assert n1.left is n1
        assert n1.right is n1
        assert n1.up is n1
        assert n1.down is n1
        assert n1.column is n1

    def test_detach_origin(self):
        origin = dlx.Node()
        left = dlx.Node()
        right = dlx.Node()
        up = dlx.Node()
        down = dlx.Node()

        origin.addAbove(up)
        origin.addBelow(down)
        origin.addLeft(left)
        origin.addRight(right)

        origin.detach()

        assert origin.up is up
        assert origin.down is down
        assert origin.left is left
        assert origin.right is right

        assert left.left is right
        assert left.right is origin

        assert right.left is origin
        assert right.right is left

        assert up.up is down
        assert up.down is down

        assert down.up is up
        assert down.down is up

    def test_attach_self(self):
        n1 = dlx.Node()
        n1.detach()
        n1.attach()

        assert n1.left is n1
        assert n1.right is n1
        assert n1.up is n1
        assert n1.down is n1
        assert n1.column is n1

    def test_attach_origin(self):
        origin = dlx.Node()
        left = dlx.Node()
        right = dlx.Node()
        up = dlx.Node()
        down = dlx.Node()

        origin.addAbove(up)
        origin.addBelow(down)
        origin.addLeft(left)
        origin.addRight(right)

        origin.detach()
        origin.attach()

        assert origin.up is up
        assert origin.down is down
        assert origin.left is left
        assert origin.right is right

        assert left.left is right
        assert left.right is origin

        assert right.left is origin
        assert right.right is left

        assert up.up is down
        assert up.down is origin

        assert down.up is origin
        assert down.down is up


class ColumnNodeTestCase(unittest.TestCase):
    def test_init(self):
        c1 = dlx.ColumnNode('c1')
        assert isinstance(c1, dlx.Node)
        assert c1.name == 'c1'
        assert c1.size == 0

        c2 = dlx.ColumnNode('c2', column=1, size=1)
        assert c2.column is c2
        assert c2.size == 1

    def test_size(self):
        column = dlx.ColumnNode('c1')
        left = dlx.Node()
        right = dlx.Node()
        up = dlx.Node()
        down = dlx.Node()

        column.addLeft(left)
        assert column.size == 0

        column.addRight(right)
        assert column.size == 0

        column.addAbove(up)
        assert column.size == 1

        column.addBelow(down)
        assert column.size == 2

    def test_iter_many(self):
        c1 = dlx.ColumnNode('c1')
        c2 = dlx.ColumnNode('c2')
        c3 = dlx.ColumnNode('c3')
        c4 = dlx.ColumnNode('c4')
        c1.addAbove(c2)
        c1.addAbove(c3)
        c1.addAbove(c4)

        self.assertEqual(list(c1), [c2, c3, c4])
        self.assertEqual(list(c2), [c3, c4, c1])
        self.assertEqual(list(c3), [c4, c1, c2])
        self.assertEqual(list(c4), [c1, c2, c3])

    def test_detach(self):
        """ Test Matrix:

             c1   c2   c3   c4   c5
            ========================
                |    | n1 | n2 | n3
            ----+----+----+----+----
             n4 |    |    |    |
            ----+----+----+----+----
                | n5 |    |    | n6
            ----+----+----+----+----
                |    | n7 |    |

        Detach c3 and it becomes:

             c1   c2   c4   c5
            ===================
                |    |    |
            ----+----+----+----
             n4 |    |    |
            ----+----+----+----
                | n5 |    | n6
            ----+----+----+----
                |    |    |
        """

        # Setup
        c1 = dlx.ColumnNode('c1')
        c2 = dlx.ColumnNode('c2')
        c3 = dlx.ColumnNode('c3')
        c4 = dlx.ColumnNode('c4')
        c5 = dlx.ColumnNode('c5')

        n1 = dlx.Node('n1')
        n2 = dlx.Node('n2')
        n3 = dlx.Node('n3')
        n4 = dlx.Node('n4')
        n5 = dlx.Node('n5')
        n6 = dlx.Node('n6')
        n7 = dlx.Node('n7')

        c1.addLeft(c2)
        c1.addLeft(c3)
        c1.addLeft(c4)
        c1.addLeft(c5)

        c1.addAbove(n4)
        c2.addAbove(n5)
        c3.addAbove(n1)
        c3.addAbove(n7)
        c4.addAbove(n2)
        c5.addAbove(n3)
        c5.addAbove(n6)

        n1.addLeft(n2)
        n1.addLeft(n3)
        n5.addLeft(n6)

        c3.detach()

        assert c2.up is n5
        assert c2.down is n5
        assert c2.left is c1
        assert c2.right is c4
        assert c2.size == 1

        assert c3.left is c2
        assert c3.right is c4
        assert c3.up is n7
        assert c3.down is n1
        assert c3.size == 2

        assert c4.up is c4
        assert c4.down is c4
        assert c4.left is c2
        assert c4.right is c5
        assert c4.size == 0

        assert c5.up is n6
        assert c5.down is n6
        assert c5.left is c4
        assert c5.right is c1
        assert c5.size == 1

    def test_attach(self):
        c1 = dlx.ColumnNode('c1')
        c2 = dlx.ColumnNode('c2')
        c3 = dlx.ColumnNode('c3')
        c4 = dlx.ColumnNode('c4')
        c5 = dlx.ColumnNode('c5')

        n1 = dlx.Node('n1')
        n2 = dlx.Node('n2')
        n3 = dlx.Node('n3')
        n4 = dlx.Node('n4')
        n5 = dlx.Node('n5')
        n6 = dlx.Node('n6')
        n7 = dlx.Node('n7')

        c1.addLeft(c2)
        c1.addLeft(c3)
        c1.addLeft(c4)
        c1.addLeft(c5)

        c1.addAbove(n4)
        c2.addAbove(n5)
        c3.addAbove(n1)
        c3.addAbove(n7)
        c4.addAbove(n2)
        c5.addAbove(n3)
        c5.addAbove(n6)

        n1.addLeft(n2)
        n1.addLeft(n3)
        n5.addLeft(n6)

        c3.detach()
        c3.attach()

        assert c2.up is n5
        assert c2.down is n5
        assert c2.left is c1
        assert c2.right is c3
        assert c2.size == 1

        assert c3.left is c2
        assert c3.right is c4
        assert c3.up is n7
        assert c3.down is n1
        assert c3.size == 2

        assert c4.up is n2
        assert c4.down is n2
        assert c4.left is c3
        assert c4.right is c5
        assert c4.size == 1

        assert c5.up is n6
        assert c5.down is n3
        assert c5.left is c4
        assert c5.right is c1
        assert c5.size == 2


class MatrixTestCase(unittest.TestCase):
    def test_zero_solutions(self):
        m = dlx.Matrix([
            [1, 1, 0],
            [1, 0, 1],
            [0, 1, 1]
        ])

        results = m.solve()
        assert len(results) == 0

    def test_one_solution(self):
        m = dlx.Matrix([
            [0, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 0, 1],
        ])

        results = m.solve()
        assert results and len(results) == 1

        rows = [n.row_index for n in results[0]]
        rows.sort()
        self.assertEqual(rows, [0, 3, 4])

    def test_two_solution(self):
        m = dlx.Matrix([
            [1, 1, 0],
            [1, 0, 1],
            [0, 0, 1],
            [0, 1, 0]
        ])

        results = m.solve()
        assert results and len(results) == 2

        result1 = map(lambda r: r.name, results[0])
        result1.sort()

        result2 = map(lambda r: r.name, results[1])
        result2.sort()

        self.assertEqual(result1, [11, 33])
        self.assertEqual(result2, [21, 42])
