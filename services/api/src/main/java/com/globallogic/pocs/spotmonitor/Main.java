package com.globallogic.pocs.spotmonitor;

import org.glassfish.grizzly.http.server.HttpServer;
import org.glassfish.jersey.grizzly2.httpserver.GrizzlyHttpServerFactory;
import org.glassfish.jersey.server.ResourceConfig;

import java.io.IOException;
import java.net.URI;

import java.util.concurrent.CountDownLatch;

import org.apache.log4j.Logger;

/**
 * Main class.
 *
 */
public class Main {


    private static final Logger logger = Logger.getLogger(Main.class);

    // Base URI the Grizzly HTTP server will listen on
    public static final String BASE_URI = "http://0.0.0.0:8080/";

    /**
     * Starts Grizzly HTTP server exposing JAX-RS resources defined in this application.
     * @return Grizzly HTTP server.
     */
    public static HttpServer createServer() {
        logger.info("Grizzly server URL " + BASE_URI);
        // create a resource config that scans for JAX-RS resources and providers
        // in com.globallogic.pocs.spotmonitor package
        final ResourceConfig rc = new ResourceConfig().packages("com.globallogic.pocs.spotmonitor");
        //rc.register(GensonJsonConverter.class);
        //rc.register(new CORSFilter());

        // create and start a new instance of grizzly http server
        // exposing the Jersey application at BASE_URI
        return GrizzlyHttpServerFactory.createHttpServer(URI.create(BASE_URI), rc);
    }

    /**
     * Main method.
     * @param args
     * @throws IOException
     */
    public static void main(String[] args) throws IOException {
/*
        final HttpServer server = startServer();
        System.out.println(String.format("Jersey app started with WADL available at "
                + "%sapplication.wadl\nHit enter to stop it...", BASE_URI));
        System.in.read();
        server.stop();
*/

    logger.info("Initiliazing Grizzly server using " + BASE_URI);
    CountDownLatch exitEvent = new CountDownLatch(1);
    HttpServer server = createServer();
    // register shutdown hook
    Runtime.getRuntime().addShutdownHook(new Thread(() -> {
      logger.info("Stopping server ...");
      server.stop();
      exitEvent.countDown();
    }, "shutdownHook"));

    try {
      server.start();
      logger.info(String.format("Jersey app started with WADL available at %sapplication.wadl", BASE_URI));
      logger.info("Press CTRL^C to exit ...");
      exitEvent.await();
      logger.info("Exiting service ...");
    } catch (InterruptedException e) {
      logger.error("There was an error while starting Grizzly HTTP server.", e);
      Thread.currentThread().interrupt();
    }






    }
}

