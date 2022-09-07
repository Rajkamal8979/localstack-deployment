insert into organization_role_snap(role_uuid,organization_uuid,organization_name,role_name,created_at,operation,last_modified_at)
select role_uuid,organization_uuid,organization_name,role_name,created_at,operation,current_timestamp
from(

select oor.role_uuid,oor.organization_uuid,oo.organization_name,oor.role_name,oor.created_at,oor.operation
from organization_role oor join organization oo on oo.organization_uuid = oor.organization_uuid
) snap_table
on conflict(role_uuid,organization_uuid)
do update
set organization_name = excluded.organization_name,
role_name = excluded.role_name,
created_at = excluded.created_at,
operation = excluded.operation,
last_modified_at = current_timestamp;
