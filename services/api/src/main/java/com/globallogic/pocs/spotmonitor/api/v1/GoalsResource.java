package com.globallogic.pocs.spotmonitor.api.v1;


import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.lang.reflect.*;

import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.PATCH;
import javax.ws.rs.DELETE;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.QueryParam;
import javax.ws.rs.DefaultValue;
import javax.ws.rs.Consumes;
import javax.ws.rs.Produces;

import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.GenericEntity;
import javax.ws.rs.core.PathSegment;

import org.apache.log4j.Logger;

import com.globallogic.pocs.spotmonitor.api.Utils;
import com.globallogic.pocs.spotmonitor.api.ApiResponse;


/**
 * 
 */
@Path("api/v1/goals")
public class GoalsResource {

  private static final Logger logger = Logger.getLogger(GoalsResource.class);

  /**
   * Create goals
   */
  @POST
  @Consumes(MediaType.APPLICATION_JSON)
  @Produces(MediaType.APPLICATION_JSON)
  @Path("/detect")
  public Response createContact(@Context UriInfo uriInfo) {
    logger.info(uriInfo.getRequestUri());
    ApiResponse r = Utils.exec(new String[]{
                      "python",
                      "./scripts/goals/detect/main.py"
                    });
    Response.Status status = Response.Status.BAD_REQUEST;
    if (r.isSucceeded()){
      status = Response.Status.OK;
    }
    return Response.status(status).entity(r).build();
  }

}
