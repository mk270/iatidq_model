
from iatidq import db
from models import *
from sqlalchemy import func

def get_package_data(package_name):
    # Get package data
    package = db.session.query(Package,
                               PackageGroup
                               ).filter(Package.package_name == package_name
                                        ).outerjoin(PackageGroup).first()
    return package

def import_pc_row(request, row):
    def pc_form_value(key):
        form_key = 'pc[%s][%s]' % (row, key)
        return request.form[form_key]

    organisation_id = pc_form_value('organisation_id')
    test_id = pc_form_value('test_id')
    operation = pc_form_value('operation')
    condition = pc_form_value('condition')
    condition_value = pc_form_value('condition_value')

    pc = OrganisationCondition.query.filter_by(
        organisation_id=organisation_id, test_id=test_id, 
        operation=operation, condition=condition, 
        condition_value=condition_value).first()

    with db.session.begin():
        if (pc is None):
            pc = OrganisationCondition()
        
        pc.organisation_id=organisation_id
        pc.test_id=test_id
        pc.operation = operation
        pc.condition = condition
        pc.condition_value = condition_value
        pc.description = pc_form_value('description')
        db.session.add(pc)

def get_distinct_conditions():
    return db.session.query(
        OrganisationCondition.description).distinct().all()

def get_package_runtime(package_id):
    return db.session.query(
        func.max(InfoResult.runtime_id)).filter(
        InfoResult.package_id == package_id
        ).first()

def all_packages():
    return db.session.query(Package).all()

def get_results():
    session = db.session
    return session.query(func.count(Result.id),
                         Result.result_data,
                         Result.test_id
            ).group_by(Result.test_id
            ).group_by(Result.result_data).all()

def mapped_tests():
    return map(lambda x: x.as_dict(),
               db.session.query(Test).all()
               )

def get_test(test_id):
    return db.session.query(Test).filter(Test.id == test_id).first()

def get_package_results():
    session = db.session
    return session.query(func.count(Result.id),
                         Result.result_data,
                         Result.package_id
            ).group_by(Result.package_id
            ).group_by(Result.result_data).all()

def get_package_by_name(package_name):
    return db.session.query(Package).filter(Package.package_name == 
                                            package_name).first()

def latest_runtime(package):
    return db.session.query(Runtime
        ).filter(Result.package_id==package.id
        ).join(Result
        ).order_by(Runtime.id.desc()
        ).first()

def test_results_h(package_name, latest_runtime, test_id, hierarchy_id):
    return db.session.query(Result.result_identifier, 
                            Result.result_data
            ).filter(Package.package_name == package_name, 
                     Result.runtime_id==latest_runtime.id, 
                     Result.test_id==test_id,
                     Result.result_hierarchy==hierarchy_id
            ).join(Package
            ).all()

def test_results(package_name, latest_runtime, test_id):
    return db.session.query(Result.result_identifier, 
                            Result.result_data
            ).filter(Package.package_name == package_name, 
                     Result.runtime_id==latest_runtime.id, 
                     Result.test_id==test_id
            ).join(Package
            ).all()

def packagegroup_by_name(packagegroup_name):
    return db.session.query(PackageGroup).filter(PackageGroup.name == 
                                                 packagegroup_name).first()

# This is crude because it assumes there is only one result for this
# test per activity-identifier. But that should be the case anyway.
def get_test_count_h(packagegroup_name, test_id, hierarchy_id):
    return db.session.query(func.count(Result.result_identifier)
            ).filter(PackageGroup.name == packagegroup_name, 
                     Result.test_id==test_id,
                     Result.result_hierarchy==hierarchy_id
            ).join(Package
            ).join(PackageGroup
            ).all()

def get_test_results_h(packagegroup_name, test_id, hierarchy_id):
    return db.session.query(Result.result_identifier, 
                                        Result.result_data,
                                        func.max(Result.runtime_id)
            ).filter(PackageGroup.name == packagegroup_name, 
                     Result.test_id==test_id,
                     Result.result_hierarchy==hierarchy_id
            ).group_by(Result.result_identifier
            ).group_by(Result.result_data
            ).join(Package
            ).join(PackageGroup
            ).limit(50
            ).offset(offset
            ).all()

def get_test_count(packagegroup_name, test_id):
    return db.session.query(func.count(Result.result_identifier)
            ).filter(PackageGroup.name == packagegroup_name, 
                     Result.test_id==test_id
            ).join(Package
            ).join(PackageGroup
            ).all()

def get_test_results(packagegroup_name, test_id):
    return db.session.query(Result.result_identifier, 
                                        Result.result_data,
                                        func.count(Result.runtime_id)
            ).filter(PackageGroup.name == packagegroup_name, 
                     Result.test_id==test_id
            ).group_by(Result.result_identifier
            ).join(Package
            ).join(PackageGroup
            ).limit(50
            ).offset(offset
            ).all()

def get_org_test_results_h(organisation_code, test_id, hierarchy_id):
    return db.session.query(Result.result_identifier, 
                                        Result.result_data,
                                        func.max(Result.runtime_id)
            ).filter(Organisation.organisation_code == organisation_code, 
                     Result.test_id==test_id,
                     Result.result_hierarchy==hierarchy_id
            ).group_by(Result.result_identifier
            ).group_by(Result.result_data
            ).join(Package
            ).join(OrganisationPackage
            ).join(Organisation
            ).limit(50
            ).offset(offset
            ).all()

def get_org_test_results(organisation_code, test_id):
    return db.session.query(Result.result_identifier, 
                                        Result.result_data,
                                        func.max(Result.runtime_id)
            ).filter(Organisation.organisation_code == organisation_code, 
                     Result.test_id==test_id
            ).group_by(Result.result_identifier
            ).join(Package
            ).join(OrganisationPackage
            ).join(Organisation
            ).limit(50
            ).offset(offset
            ).all()

def get_active_packages():
    return Package.query.filter_by(active=True).all()

def organisation_by_code(organisation_code):
    return Organisation.query.filter(Organisation.organisation_code ==
                                     organisation_code
                                     ).first()

def all_organisations():
    return Organisation.query.order_by(Organisation.organisation_code).all()

def all_organisations_unsorted():
    return Organisation.query.all()

def get_organisation_condition(pc_id):
    return OrganisationCondition.query.filter_by(id=pc_id).first()

def tests_in_order():
    return Test.query.order_by(Test.id).all()

def new_organisation_condition():
    return OrganisationCondition()

def organisation_condition_by_id(oc_id):
    return OrganisationCondition.query.filter_by(id=oc_id).first()

def packages_in_order():
    return Package.query.order_by(Package.package_name).all()

def active_packages_in_order():
    return Package.query.filter_by(active=True).order_by(
        Package.package_name).all()

