create table if not exists hubspot_contacts (
    hs_object_id bigint primary key,
    email text,
    firstname text,
    lastname text,
    createdate timestamptz,
    lastmodifieddate timestamptz,
    _ingested_at timestamptz default now()
);

create table if not exists hubspot_deals (
    hs_object_id bigint primary key,
    dealname text,
    amount numeric,
    dealstage text,
    pipeline text,
    createdate timestamptz,
    hs_lastmodifieddate timestamptz,
    _ingested_at timestamptz default now()
);
