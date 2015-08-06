--------------------------------------------
BEGIN;
	DO
	$do$
		BEGIN
            IF EXISTS(SELECT 1 FROM "wos_master" WHERE "wos_uid" = '%pkey%' AND "file_number" <= %file_number%)
                THEN
                    DELETE FROM "wos_master" WHERE "wos_uid" = '%pkey%';
            END IF;
            IF NOT EXISTS(SELECT 1 FROM "wos_master" WHERE "wos_uid" = '%pkey%' AND "file_number" > 1)
				THEN
%data%
			END IF;
		END
	$do$;
COMMIT;



