#!/usr/bin/env python3
from contextlib import contextmanager
import datetime

import sqlalchemy
from sqlalchemy import (
    Column, Integer, String, Table, create_engine, BigInteger,
    Text, DateTime, DECIMAL, BOOLEAN, ForeignKey, DDL
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import relationship

# connection_string = 'postgresql://username[:password]@host[:port]/dbname'
# schema_name = 'stuff'
schema_name = 'stuff'

engine = create_engine('postgresql://violet@192.168.2.32:54321/postgres')
create_str = "CREATE DATABASE %s ;" % (schema_name,)
conn = engine.connect()
try:
    conn.execution_options(isolation_level="AUTOCOMMIT").execute(create_str)
except sqlalchemy.exc.ProgrammingError:
    pass
finally:
    conn.close()

engine = create_engine('postgresql://violet@192.168.2.32:54321/stuff')
create_schema_str = "CREATE SCHEMA IF NOT EXISTS %s;" % (schema_name,)
conn = engine.connect()
try:
    conn.execution_options(isolation_level="AUTOCOMMIT").execute(create_schema_str)
    conn.close()
except sqlalchemy.exc.ProgrammingError:
    pass


SABase = declarative_base(
    metadata=MetaData(
        bind=engine,
        schema=schema_name,
    ),
)


def create_tables():
    # engine.execute(DDL('CREATE SCHEMA IF NOT EXISTS {schema}'.format(
    #     schema=schema_name,
    # )))
    # engine.execute(DDL('CREATE SCHEMA IF NOT EXISTS {schema}'.format(
    #     schema=schema_name,
    # )))
    # conn = engine.connect()
    SABase.metadata.create_all()


def drop_tables():
    SABase.metadata.drop_all()


def pkey(id_str, dtype=Integer):
    return Column(
        id_str,
        dtype,
        autoincrement=True,
        primary_key=True,
    )


def datetime_col(colname):
    return Column(
        colname,
        DateTime,
        nullable=False,
        # default="date_trunc('second', now())::timestamp",
        default="NOW()",
    )


class Base:
    created = datetime_col('created')
    modified = datetime_col('modified')

    def __init__(self, time=None):
        if time is None:
            time = datetime.datetime.now().replace(microsecond=0)
        self.created_at = self.modified_at = time

    @staticmethod
    def get_col_name(col):
        return str(col).split('.')[-1]

    @classmethod
    def get_row(cls, col, value, sess):
        query = sess.query(cls).filter(col==value)

        # if it exists, then return it
        row = query.one_or_none()
        if row is not None:
            return row

        # otherwise, create one
        row = cls()
        setattr(
            row,
            cls.get_col_name(col),
            value
        )

        # make sure the row is entered into the db and
        # has its id field populated so its id can be
        # referenced
        sess.add(row)
        sess.commit()

        return row

    Session = None
    @classmethod
    def set_sess(cls, Session):
        cls.Session = Session

    @classmethod
    @contextmanager
    def get_session(cls, sess=None):
        """
        Note that operations that create rows in
        multiple tables at once need to share
        the same session.
        """
        if sess is None:
            managed = True
            if cls.Session is None:
                raise Exception(
                    "session not set. must be set using Base.set_sess(sqlalchemy.orm.sessionmaker(bind=engine))"
                )
            sess = cls.Session()
        else:
            managed = False
        try:
            yield sess
        except KeyboardInterrupt:
            raise
        except Exception:
            # TODO not sure whether unmanaged session should be rolled back
            sess.rollback()
        else:
            if managed:
                sess.commit()
        finally:
            if managed:
                sess.close()

    def __repr__(self):
        """Generic repr method for 
        """
        attrs = list()
        for k in self.__init__.__code__.co_varnames[1:]:
            if not hasattr(self, k):
                continue
            attrs.append('{}={}'.format(
                k, repr(getattr(self, k))
            ))
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(attrs),
        )

    def __str__(self):
        return repr(self)


class User(Base, SABase):
    __tablename__ = 'user'
    user_id = pkey('user_id')
    username = Column('username', Text, nullable=False)


def upgrade_database():
    import os
    import alembic
    from alembic import config

    alembic_dir = os.path.join(os.path.abspath('.'), 'alembic')
    os.chdir(alembic_dir)
    ini_filepath = os.path.join(alembic_dir, 'alembic.ini')

    cmdline = config.CommandLine()
    options = cmdline.parser.parse_args(['upgrade', 'head'])
    cfg = config.Config(
        file_=ini_filepath,
        ini_section=options.name,
        cmd_opts=options,
    )
    alembic.command.upgrade(cfg, 'head')


if __name__ == '__main__':
    Base.set_sess(sqlalchemy.orm.sessionmaker(bind=engine))
    create_tables()
    with Base.get_session() as sess:
        sess.commit()

    print("upgrading database")
    upgrade_database()
