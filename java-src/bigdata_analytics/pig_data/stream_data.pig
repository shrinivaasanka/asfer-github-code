stre_dat = LOAD 'hdfs:/user/root/stream.data' USING PigStorage(',') AS (
           alphanum:chararray
);
/*dump stre_data;*/
STORE stre_dat INTO 'hbase://stream_data' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage(
'cf:alphanum' 
);

stre_dat = load 'movielens_stream.data' using PigStorage('\n') AS (alphanum:chararray);
STORE stre_dat INTO 'hbase://stream_data' USING org.apache.pig.backend.hadoop.hbase.HBaseStorage('cf:alphanum') AS ('cf:alphanum');
