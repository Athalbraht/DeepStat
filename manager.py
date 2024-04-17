from addons import fm
from texbuilder import Section
from conf import structure
from typing import Protocol


class FlagStrategy(Protocol):
    pass


class Order():

    def __init__(self, flg, kind, ctx, mode, loc):
        self.flg = flg
        self.kind = kind
        self.ctx = ctx
        self.mode = mode
        self.loc = loc


class OrderObject():

    def __init__(self, id, flg, kind, ctx, mode, loc):
        self.id = id
        self.flg = flg
        self.kind = kind
        self.ctx = ctx
        self.mode = mode
        self.loc = loc

        self.calculated = False

    def create_command(self):
        pass


    def __repr__(self):
        return "{}:{}:{}:{}:{}".format(
            self.id,
            self.flg,
            self.kind,
            self.ctx,
            self.mode,
        )


class Loader():
    """Loader class."""

    def __init__(self):
        self.instructions = []
        self.queue = []
        self.last_id = 0
        """Translate user instructions to func execute type."""

    def open_file(self, ctx):
        pass

    def generate(self, ctx):
        pass

    def load(self, ctx):
        pass

    def create_id(self):
        self.last_id += 1
        return self.last_id

    def obj(self, flg, kind, ctx, mode='static', loc='inline', *args, **kwargs):
        """"""

        print("\t- Registering {} as {} for {} in {} mode".format(
            fm(kind),
            fm(flg, 'yellow'),
            fm(ctx, 'cyan'),
            fm(mode, 'red')))
        orderID = self.create_id()
        params = {
            "id" : orderID,
            "flg" : flg,
            "kind" : kind,
            "ctx" : ctx,
            "mode" : mode,
            "loc" : loc,
        }
        _obj = OrderObject(**params)
        self.instructions.append(_obj)
        return _obj

        # if flg == 'file':
        #    self.open_file(ctx)
        # elif flg == 'load':
        #    self.load(ctx)
        # elif flg == 'gen':
        #    self.generate(ctx)

        # if kind == 'desc':
        #    pass
        # elif kind == 'plot':
        #    pass
        # elif kind == 'table':
        #    pass

        # return tex_order
        # nr = 'random'
        # nu = 'uniqe'
        # ng = 'global'
        # ns = 'static'
        # np = 'paraphrase'
        # pass

    def organize(self):
        """Define priority of instructions."""
        print("\t- Sorting instructions list")
        high = []
        medium = []
        low = []
        for i in self.instructions:
            pass
        high.extend(medium)
        high.extend(low)
        self.queue = high

    def execute_queue(self):
        print("\t- Executing analysis instructions")
        pass


class Session:
    """DOCssd."""

    def __init__(self, tex_config):
        """Session manager for analysis session."""
        self.loader = Loader()
        self.document = Section("Report", config=tex_config, init=True)
        self.structure = structure(self.loader)

    def create_table_of_content(self):
        """Wrap tex build."""
        self.document.build(self.structure, self.document)

    def boost_instructions(self):
        self.loader.organize()
        self.loader.execute_queue()

    def queue_organizer(self, queue):
        """Organize analysis instruction based on priority of funcions."""
