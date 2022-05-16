from datetime import datetime

import sqlalchemy as _sa
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class RecordTimestampFields:
    """
    Collection of record edition timestamps
    They are common for many models
    """

    record_created = _sa.Column(
        _sa.DateTime,
        nullable=False,
        default=datetime.now,
        server_default=_sa.text("statement_timestamp()"),
    )

    record_modified = _sa.Column(
        _sa.DateTime,
        nullable=False,
        default=datetime.now,
        server_default=_sa.text("statement_timestamp()"),
        onupdate=datetime.now,
        index=True,
    )
