package com.globallogic.pocs.spotmonitor.api;

import java.util.List;
import java.util.ArrayList;

public class ApiResponse {
  //
  private int code = 0;
  public int getCode() { return this.code; }
  public boolean isSucceeded() { return (this.code == 0); }
  //
  private String message = "";
  public String getMessage() { return this.message; }
  //
  private List<Object> data = null;
  public List<Object> getData() { return this.data; }

  /**
   *
   */
  public ApiResponse() {
  }

  /**
   *
   */
  public static ApiResponse build() {
    return build(0, "");
  }
  /**
   *
   */
  public static ApiResponse build(final int code) {
    ApiResponse response = new ApiResponse();
    response.code = code;
    return response;
  }

  /**
   *
   */
  public static ApiResponse build(final int code, final String message) {
    ApiResponse response = ApiResponse.build(code);
    response.message = message;
    return response;
  }

  /**
   *
   */
  public static ApiResponse build(final String message) {
    ApiResponse response = ApiResponse.build(0);
    response.message = message;
    return response;
  }

  /**
   *
   */
  public static ApiResponse buildList(final int code, final String message, final List<Object> data) {
    ApiResponse response = build(code, message);
    response.data = data;
    return response;
  }

  /**
   *
   */
  public static ApiResponse buildList(final List<Object> data) {
    ApiResponse response = build(0, "");
    response.data = data;
    return response;
  }

  /**
   *
   */
  public static ApiResponse build(final Object data) {
    return buildList(new ArrayList<Object>(){{ add(data); }} );
  }
}

