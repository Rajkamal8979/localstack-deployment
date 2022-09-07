create table if not exists organization_role_summary_snap(
    role_uuid varchar(100),
    organization_uuid varchar(100),
    organization_name varchar(100),
    role_name varchar(100),
    member_count integer,
    role_count integer
    );
