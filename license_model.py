"""License model class."""
from __future__ import annotations

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from model.entity.license_db.license_permits import LicensePermit
from model.entity.license_db.license_permits import LicenseTypeAttribute
from model.entity.license_db.license_type_permits import LicenseType
from model.entity.license_db.license_type_permits import LicenseTypePermit
from model.entity.license_db.license_type_vertical_techniques import LicenseTypeVerticalTechnique
from model.entity.license_db.license_type_verticals import LicenseTypeVertical
from model.repository.db_model import DBModel


class LicenseModel(DBModel):

    """LicenseModel class."""

    def __init__(self) -> None:
        """To initialize the Constructor method."""
        super().__init__()
        self.connection = self.connect('LicenseDB')
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = self.session_maker()

    def get_license_type_names(self, license_type_id: list) -> str:
        """Get license type name information."""
        result = self.session.query(
            LicenseTypeAttribute.type_value,
            LicenseType.license_type_id,
        ).distinct().join(LicenseTypeAttribute,
                          LicenseType.name_id == LicenseTypeAttribute.license_type_attribute_id).where(
            LicenseType.license_type_id.in_(license_type_id),
            LicenseTypeAttribute.status == 1,
        ).all()
        return '\n'.join([license_type[0] for license_type in result])

    def get_license_permit_names(self, license_type_permit_id: list) -> str:
        """Get permit name information."""
        result = self.session.query(
            LicenseTypeAttribute.type_value,
            LicenseTypePermit.license_type_permit_id,
            LicensePermit.permit_name_id,
        ).distinct().join(LicensePermit,
                          LicenseTypePermit.license_permit_id == LicensePermit.license_permit_id
                          ).join(LicenseTypeAttribute,
                                 LicensePermit.permit_name_id == LicenseTypeAttribute.license_type_attribute_id).where(
            LicenseTypePermit.license_type_permit_id.in_(
                license_type_permit_id),
            LicenseTypeAttribute.status == '1',
        ).all()
        permit_names = [permit_name[0] for permit_name in result]
        return '\n'.join(set(permit_names))

    def get_license_vertical_names(self, license_vertical_id: list) -> str:
        """Get vertical name information."""
        result = self.session.query(
            LicenseTypeAttribute.type_value,
            LicenseTypeVertical.license_type_vertical_id,
        ).distinct().join(LicenseTypeAttribute,
                          LicenseTypeVertical.vertical_name_id == LicenseTypeAttribute.license_type_attribute_id).where(
            LicenseTypeVertical.license_type_vertical_id.in_(
                license_vertical_id),
            LicenseTypeAttribute.status == '1',
        ).all()
        vertical_names = [vertical_name[0] for vertical_name in result]
        return '\n'.join(set(vertical_names))

    def get_license_vertical_technique_names(self, license_vertical_technique_id: list) -> str:
        """Get vertical_technique name information."""
        query = db.select([LicenseTypeVerticalTechnique.technique_name,
                           ]).distinct().where(
            LicenseTypeVerticalTechnique.license_type_vertical_technique_id.in_(license_vertical_technique_id))
        resp = self.connection.execute(query).fetchall()
        technique_names = [technique_names[0] for technique_names in resp]
        return '\n'.join(set(technique_names))
