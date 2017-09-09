package java_demo_web_client;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class DemoClient {
	
	
	public String getFromURL(String serverUrl, String markcode){
		String ret = "";		
		HttpURLConnection httpconn= null;
		try {
			URL url = new URL(serverUrl+ "/" + markcode);
			httpconn = (HttpURLConnection) url.openConnection() ;
//			httpconn.setRequestProperty("Accept-Charset", "utf-8");
//			httpconn.setRequestProperty("Content-Type", "application/json");
//			httpconn.setRequestMethod("GET");
			httpconn.connect();
			InputStreamReader inreader = new InputStreamReader(httpconn.getInputStream(),"utf-8");
			BufferedReader reader = new BufferedReader(inreader);
			String lines = null;
			while( (lines = reader.readLine()) != null ){
				ret += lines ;
			}
			
		} catch (Exception e) {
			e.printStackTrace(); 
		}
		
		return ret;
	}

	public static void main(String[] args) {
		String serverUrl = "http://localhost:7856/demk";
		serverUrl = "http://106.14.57.192:7856/demk";
		String markcode = "009763F220C61E7C";
		// 读取文件取得 markcode
		// 需要校验 markcode 并过滤掉非法的； 以免干扰使得程序中断， 
		//  markcode == 16 /32 位 中间无空格， 0-9 a-f 字串
		// 
		DemoClient demo = new DemoClient();
		String result = demo.getFromURL(serverUrl, markcode);
		System.out.print( result);

	}

}
