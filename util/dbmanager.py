# coding:utf-8
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base


class DBManager(object):
    def __init__(self):
        self.engine_map = {}
        self.session_map = {}
        self.autobaseobj = {}
        self.app = None
        self.alias = []

    def init_app(self, app):
        self.app = app
        self.create_sessions(app)

    def create_sessions(self, app):
        db_settings = app.config['SQLALCHEMY_DATABASE_URI_SETTINGS']
        for dbalias, dbinfo in db_settings.items():
            self.alias.append(dbalias)
            self.engine_map[dbalias] = {}
            self.session_map[dbalias] = {}
            self.autobaseobj[dbalias] = {}
            for role, urls in dbinfo.items():
                self.engine_map[dbalias][role] = []
                self.session_map[dbalias][role] = []
                self.autobaseobj[dbalias][role] = []
                for url in urls:
                    engine, single_session = self.create_single_session(url)
                    autobase = automap_base()
                    autobase.prepare(engine, reflect=True)
                    self.autobaseobj[dbalias][role].append({
                        "engine": engine,
                        "autobase": autobase,
                    })
                    self.engine_map[dbalias][role].append(engine)
                    self.session_map[dbalias][role].append(single_session)

    @classmethod
    def create_single_session(cls, url, scopefunc=None):
        engine = create_engine(url, pool_recycle=7200, pool_size=50)
        return engine, scoped_session(sessionmaker(expire_on_commit=False, bind=engine), scopefunc=scopefunc)

    def get_session(self, name, dbalias):
        try:
            if not name:
                # 当没有提供名字时，我们默认为读请求，
                name = 'slave'
            # 现在的逻辑是在当前所有的配置中随机选取一个数据库，
            return random.choice(self.session_map[dbalias][name])
        except KeyError:
            raise KeyError('{} not created, check your DB_SETTINGS'.format(name))
        except IndexError:
            raise IndexError('cannot get names from DB_SETTINGS')

    def get_engine_master(self, dbalias):
        return random.choice(self.engine_map[dbalias]['master'])

    def get_autobase_obj(self, dbalias):
        return self._ab_master(dbalias)

    def master(self, dbalias="default"):
        return random.choice(self.session_map[dbalias]['master'])

    def slave(self, dbalias="default"):
        return random.choice(self.session_map[dbalias]['slave'])

    def session_ctx(self, dbalias, bind=None):
        db_session = self.get_session(bind, dbalias)
        session = db_session()
        session._model_changes = {}    # ???
        return session

    def autobase(self):
        return self.autobaseobj

    def _ab_slave(self, dbalias):
        return random.choice(self.autobaseobj[dbalias]['slave'])

    def _ab_master(self, dbalias):
        return random.choice(self.autobaseobj[dbalias]['master'])

    def get_table(self, tname, dbalias):
        if dbalias not in self.alias:
            return False, "dbalias not exists"
        abobj = db_manager._ab_master(dbalias)
        try:
            table_obj = getattr(abobj['autobase'].classes, tname)
        # except AttributeError as e:
        #     pass
        except Exception as e:
            return False, f"Exception: {e}"
        return True, table_obj

    def test_table(self, tname, dbalias):
        if dbalias not in self.alias:
            return None
        abobj = db_manager._ab_master(dbalias)
        try:
            table = abobj['autobase'].metadata.tables[tname]
        except Exception as e:
            return False
        return True

    def flush_autobase(self, dbalias):
        for name, objs in self.autobaseobj[dbalias].items():
            for obj in objs:
                obj['autobase'] = automap_base()
                obj['autobase'].prepare(obj['engine'], reflect=True)

    def dbs_alias_list(self):
        return self.alias


class DBProxy(object):
    db_session_manager = None
    write_db = None
    read_db = None

    def __init__(self, db_session_manager=None):
        self.app = None
        self.db_session_manager = db_session_manager

    def init_app(self, app):
        self.app = app

    def init_db_session(self, action='r'):
        # action in ['r', 'w', 'rw']
        try:
            self.write_db = self.db_session_manager.session_ctx(bind='master')
            self.read_db = self.db_session_manager.session_ctx()
            # 根据user_id 处理连接
            # e.g. self.write_db.execute('use db_' + user_id)
        except Exception as e:
            self.app.logger.exception('info')
        return


db_manager = DBManager()




