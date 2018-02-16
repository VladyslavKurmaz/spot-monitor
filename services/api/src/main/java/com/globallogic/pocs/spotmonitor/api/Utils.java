package com.globallogic.pocs.spotmonitor.api;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import javax.ws.rs.core.Response;

import java.util.Optional;
import org.apache.log4j.Logger;
import com.owlike.genson.Genson;

import com.globallogic.pocs.spotmonitor.api.ApiResponse;

/**
 * Main class.
 *
 */
public class Utils {
  //
  private static final Logger logger = Logger.getLogger(Utils.class);

  /**
   */
  public static ApiResponse exec(final String[] args){
    logger.info("[+] Executing: " + String.join(" ", args));
    int exitVal = -1;
    String result = "";
    try {
      Process p = Runtime.getRuntime().exec(args);
      BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));
      String line = "";
      while ((line = reader.readLine())!= null) {
        result += line;
      }
      exitVal = p.waitFor();
      logger.info("Finished: " + exitVal);
    } catch (Exception e) {
      exitVal = Response.Status.INTERNAL_SERVER_ERROR.getStatusCode();
      result = e.getMessage();
      logger.error("Execution error", e);
    }
    logger.info("Exit code: " + (new Integer(exitVal)).toString());
    logger.info("Output: " + result);
    logger.info("[-]");
    if (exitVal == 0){
      try{
        return ApiResponse.build((new Genson()).deserialize(result, Object.class));
      } catch (Exception e) {
        return ApiResponse.build(Response.Status.INTERNAL_SERVER_ERROR.getStatusCode(), e.getMessage());
      }
    }
    return ApiResponse.build(exitVal, "Exit code: " + (new Integer(exitVal)).toString() + " " + result);
  }

}
