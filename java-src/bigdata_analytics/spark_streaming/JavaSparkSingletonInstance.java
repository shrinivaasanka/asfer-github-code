import org.apache.spark.sql.SparkSession;
import org.apache.spark.SparkConf;


public class JavaSparkSingletonInstance
{
	private static transient SparkSession instance=null;
	
	public static SparkSession getInstance(SparkConf sparkConf)
	{
		if(instance==null)
		{
			instance=SparkSession
					.builder()
					.config(sparkConf)
					.enableHiveSupport()
					.getOrCreate();
		}
		return instance;
	}
}
