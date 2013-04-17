class Node(object):

    def __init__(self,
                 name=None,
                 column=None,
                 left=None,
                 right=None,
                 up=None,
                 down=None):
        self.name = name
        self.column = column or self
        self.left = left or self
        self.right = right or self
        self.up = up or self
        self.down = down or self

    def __iter__(self):
        return self.irow

    @property
    def icolumn(self):
        node = self.down
        while node != self:
            yield node
            node = node.down

    @property
    def irow(self):
        node = self.right
        while node != self:
            yield node
            node = node.right

    def addAbove(self, node):
        node.down = self
        node.up = self.up
        node.column = self.column
        self.up.down = node
        self.up = node

        if hasattr(self.column, 'size'):
            self.column.size += 1

    def addBelow(self, node):
        node.up = self
        node.down = self.down
        node.column = self.column
        self.down.up = node
        self.down = node

        if hasattr(self.column, 'size'):
            self.column.size += 1

    def addLeft(self, node):
        node.right = self
        node.left = self.left
        self.left.right = node
        self.left = node

    def addRight(self, node):
        node.left = self
        node.right = self.right
        self.right.left = node
        self.right = node

    def detach(self):
        self.detach_column()

    def detach_column(self):
        self.up.down = self.down
        self.down.up = self.up

        if hasattr(self.column, 'size'):
            self.column.size -= 1

    def detach_row(self):
        self.left.right = self.right
        self.right.left = self.left

    def attach(self):
        self.attach_column()

    def attach_column(self):
        self.up.down = self
        self.down.up = self

        if hasattr(self.column, 'size'):
            self.column.size += 1

    def attach_row(self):
        self.left.right = self
        self.right.left = self

    def __repr__(self):
        if self.name:
            return '%s' % self.name
        return super(Node, self).__repr__()


class ColumnNode(Node):

    def __init__(self, name, size=0, **kw):
        kw['column'] = self
        super(ColumnNode, self).__init__(**kw)
        self.name = name
        self.size = size

    def __iter__(self):
        return self.icolumn

    def detach(self):
        self.detach_row()

        for node in self:
            for cell in node:
                cell.detach_column()

    def attach(self):
        for node in self:
            for cell in node:
                cell.attach_column()

        self.attach_row()


class Matrix(object):
    root = None
    solutions = None

    def __init__(self, source=None):
        self.hidden = []

        if source:
            self.build(source)

    def build(self, source):
        self.solutions = None
        root = ColumnNode('root')
        columns = [root]
        self.root = root

        for i, row in enumerate(source):
            node = None

            for j, cell in enumerate(row):

                if len(columns) <= (j + 1):
                    name = 'c%s' % (j + 1)
                    column = ColumnNode(name)
                    columns[-1].addRight(column)
                    columns.append(column)

                if not cell:
                    continue

                name = int('%s%s' % (i + 1, j + 1))
                column = columns[j + 1]
                cell = Node(name=name, column=column)
                cell.row_index = i
                cell.column_index = j
                column.addAbove(cell)

                if not node:
                    node = cell
                else:
                    node.addRight(cell)

    def solve(self, force=False):
        if force:
            self.solutions = None

        if self.solutions is not None:
            return self.solutions

        self.solutions = []
        self.search()
        return self.solutions

    def search(self, selected=None):
        column = self.root.right

        if column.right == column and selected:
            self.solutions.append(selected[:])

        if column.size < 1:
            return

        selected = selected or []
        column.detach()

        for row in column:
            selected.append(row)
            for node in row:
                node.column.detach()
            self.search(selected=selected)
            for node in row:
                node.column.attach()
            selected.remove(row)

        column.attach()
        return self

    def hide(self, column):
        if column in self.hidden:
            return

        column.detach()
        for row in column:
            for node in row:
                node.column.detach()

        self.hidden.append(column)

    def show(self, column):
        if column not in self.hidden:
            return

        for row in column:
            for node in row:
                node.column.attach()

        column.attach()
        self.hidden.remove(column)


class UIMatrix(Matrix):

    @property
    def solution_matrices(self):
        if getattr(self, '_solution_matrices', None):
            return self._solution_matrices

        matrices = []
        for s in self.solutions:
            s = sorted(s, key=lambda n: n.row_index)
            s = map(lambda n: self.source[n.row_index], s)
            matrices.append(s)
        return matrices

    def build(self, source):
        self._solution_matrices = None
        source = list(source)
        super(UIMatrix, self).build(source)
        self.source = source

    def solve(self, force=False):
        if force:
            self._solution_matrices = None

        super(UIMatrix, self).solve(force=force)
        return self.solution_matrices
