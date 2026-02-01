-- Seed data for breed_variants table
-- Generated from breeds.json
-- Usage: psql -d your_database -f seed_breed_variants.sql
-- Note: Run seed_breeds.sql first to populate the breeds table

BEGIN;

-- Only insert if table is empty
DO $$
BEGIN
    IF (SELECT COUNT(*) FROM breed_variants) = 0 THEN
        -- african variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'wild' FROM breeds WHERE breed = 'african';

        -- australian variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['kelpie', 'shepherd']) FROM breeds WHERE breed = 'australian';

        -- bakharwal variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'indian' FROM breeds WHERE breed = 'bakharwal';

        -- buhund variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'norwegian' FROM breeds WHERE breed = 'buhund';

        -- bulldog variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['boston', 'english', 'french']) FROM breeds WHERE breed = 'bulldog';

        -- bullterrier variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'staffordshire' FROM breeds WHERE breed = 'bullterrier';

        -- cattledog variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'australian' FROM breeds WHERE breed = 'cattledog';

        -- chippiparai variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'indian' FROM breeds WHERE breed = 'chippiparai';

        -- collie variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'border' FROM breeds WHERE breed = 'collie';

        -- corgi variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'cardigan' FROM breeds WHERE breed = 'corgi';

        -- dane variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'great' FROM breeds WHERE breed = 'dane';

        -- danish variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'swedish' FROM breeds WHERE breed = 'danish';

        -- deerhound variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'scottish' FROM breeds WHERE breed = 'deerhound';

        -- elkhound variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'norwegian' FROM breeds WHERE breed = 'elkhound';

        -- finnish variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'lapphund' FROM breeds WHERE breed = 'finnish';

        -- frise variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'bichon' FROM breeds WHERE breed = 'frise';

        -- gaddi variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'indian' FROM breeds WHERE breed = 'gaddi';

        -- german variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'shepherd' FROM breeds WHERE breed = 'german';

        -- greyhound variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['indian', 'italian']) FROM breeds WHERE breed = 'greyhound';

        -- hound variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['afghan', 'basset', 'blood', 'english', 'ibizan', 'plott', 'walker']) FROM breeds WHERE breed = 'hound';

        -- mastiff variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['bull', 'english', 'indian', 'tibetan']) FROM breeds WHERE breed = 'mastiff';

        -- mountain variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['bernese', 'swiss']) FROM breeds WHERE breed = 'mountain';

        -- mudhol variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'indian' FROM breeds WHERE breed = 'mudhol';

        -- ovcharka variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'caucasian' FROM breeds WHERE breed = 'ovcharka';

        -- pariah variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'indian' FROM breeds WHERE breed = 'pariah';

        -- pinscher variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'miniature' FROM breeds WHERE breed = 'pinscher';

        -- pointer variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['german', 'germanlonghair']) FROM breeds WHERE breed = 'pointer';

        -- poodle variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['medium', 'miniature', 'standard', 'toy']) FROM breeds WHERE breed = 'poodle';

        -- rajapalayam variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'indian' FROM breeds WHERE breed = 'rajapalayam';

        -- retriever variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['chesapeake', 'curly', 'flatcoated', 'golden']) FROM breeds WHERE breed = 'retriever';

        -- ridgeback variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'rhodesian' FROM breeds WHERE breed = 'ridgeback';

        -- rough variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'collie' FROM breeds WHERE breed = 'rough';

        -- schnauzer variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['giant', 'miniature']) FROM breeds WHERE breed = 'schnauzer';

        -- segugio variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'italian' FROM breeds WHERE breed = 'segugio';

        -- setter variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['english', 'gordon', 'irish']) FROM breeds WHERE breed = 'setter';

        -- sheepdog variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['english', 'indian', 'shetland']) FROM breeds WHERE breed = 'sheepdog';

        -- spaniel variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['blenheim', 'brittany', 'cocker', 'irish', 'japanese', 'sussex', 'welsh']) FROM breeds WHERE breed = 'spaniel';

        -- spitz variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['indian', 'japanese']) FROM breeds WHERE breed = 'spitz';

        -- springer variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'english' FROM breeds WHERE breed = 'springer';

        -- terrier variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, unnest(ARRAY['american', 'andalusian', 'australian', 'bedlington', 'border', 'boston', 'cairn', 'dandie', 'fox', 'irish', 'kerryblue', 'lakeland', 'norfolk', 'norwich', 'patterdale', 'russell', 'scottish', 'sealyham', 'silky', 'tibetan', 'toy', 'welsh', 'westhighland', 'wheaten', 'yorkshire']) FROM breeds WHERE breed = 'terrier';

        -- waterdog variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'spanish' FROM breeds WHERE breed = 'waterdog';

        -- wolfhound variants
        INSERT INTO breed_variants (breed_id, variant)
        SELECT id, 'irish' FROM breeds WHERE breed = 'wolfhound';

        RAISE NOTICE 'Inserted breed variants successfully';
    ELSE
        RAISE NOTICE 'breed_variants table not empty, skipping seed';
    END IF;
END $$;

COMMIT;
