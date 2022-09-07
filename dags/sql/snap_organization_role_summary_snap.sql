insert into organization_role_summary_snap (role_uuid,organization_uuid,organization_name,role_name,member_count,role_count)
select role_uuid,organization_uuid,organization_name,role_name,member_count,role_count
from(
select inner_q.role_uuid,inner_q.organization_uuid,outer_q.organization_name,inner_q.role_name,sum(role_count) over(partition by inner_q.organization_uuid) as member_count,role_count from
(
select oor.organization_uuid,oor.role_uuid,oor.role_name,
count(*) as role_count
from organization_role oor
    group by oor.organization_uuid,oor.role_uuid,oor.role_name
order by oor.organization_uuid) inner_q 
join (select distinct(organization_uuid),organization_name from organization) outer_q
on inner_q.organization_uuid =outer_q.organization_uuid) snap_table
on conflict (role_uuid,organization_uuid)
do update
set organization_name = excluded.organization_name,
role_name = excluded.role_name,
member_count = excluded.member_count,
role_count = excluded.role_count;

