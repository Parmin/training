



# mmap_test_start
#!/usr/bin/env bash

DBPATH=/data/mmap_test
mkdir $DBPATH
mongod --storageEngine mmapv1 --port 30000 --smallfiles \
    --noprealloc --dbpath $DBPATH --logpath $DBPATH/mongod.log --fork
echo "var padding = 'PADDING';
for (i=1; i<=4; i++) { padding += padding }
for (j=1; j<=100000; j++) {
    docList = []; for (i=1; i<=1000; i++) {
        docList.push( { a : padding, b : padding, c : padding } )
    }; db.padding.insertMany(docList); };" | mongo --port 30000 &
ls -lah $DBPATH
sleep 3
ls -lah $DBPATH
# mmap_test_end

# TEST

