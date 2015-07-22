stre_dat = load 'movielens_stream2.data' using PigStorage(' ') AS (row:chararray, alphanum:chararray);
dump stre_dat; 
describe stre_dat;
STORE stre_dat INTO 'hbase://stream_data' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('cf:alphanum');
