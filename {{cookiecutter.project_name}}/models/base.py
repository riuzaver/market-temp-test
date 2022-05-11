from datetime import datetime

import sqlalchemy as _sa
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class RecordStateFields(object):
    """
    Collection of active/delete fields
    They are common for many models
    """

    is_active = _sa.Column(
        _sa.Boolean,
        nullable=False,
        default=True,
        server_default="TRUE",
    )

    is_deleted = _sa.Column(
        _sa.Boolean,
        nullable=False,
        default=False,
        server_default="FALSE",
        index=True,
    )

    @property
    def is_valid(self):
        return self.is_active and not self.is_deleted

    def get_record_state(self):
        status = "active"
        if not self.is_active:
            status = "in" + status
        if self.is_deleted:
            status += ", deleted"

        return status


class RecordTimestampFields(object):
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

    def get_record_timestamps(self):
        return (
            "created @ {:%Y-%m-%d %H:%M:%S}, modified @ {:%Y-%m-%d %H:%M:%S}"
        ).format(
            self.record_created,
            self.record_modified,
        )


class CommonFields(
    RecordStateFields,
    RecordTimestampFields,
):
    """
    Collection of common fields
    """

    pass
