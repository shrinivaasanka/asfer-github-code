stre_dat = load 'hdfs://localhost:9000/user/root/movielens_stream.data' using PigStorage(':') AS (alphanum:chararray);
dump stre_dat;
STORE stre_dat INTO 'stream_data' USING org.apache.hive.hcatalog.pig.HCatStorer();

stre_dat = load 'movielens_stream.data' using PigStorage('\n') AS (alphanum:chararray);
dump stre_dat;
STORE stre_dat INTO 'stream_data' USING org.apache.hive.hcatalog.pig.HCatStorer();
