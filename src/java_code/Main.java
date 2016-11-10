//package java_code;
//
//import com.sun.net.httpserver.HttpExchange;
//import com.sun.net.httpserver.HttpHandler;
//import com.sun.net.httpserver.HttpServer;
//
//import java.awt.*;
//import java.io.IOException;
//import java.io.OutputStream;
//import java.net.InetSocketAddress;
//import java.net.URI;
//import java.nio.charset.Charset;
//import java.nio.file.Files;
//import java.nio.file.Paths;
//
//public class Main {
//
//    public static void main(String[] args) throws Exception {
//        // Test to ensure file is being read
////        String response = readFile("src/html/index.html", Charset.defaultCharset());
////        System.out.println(response);
//
//        String indexName = "backup";
//
//
//        HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
//        server.createContext("/" + indexName, new MyHandler());
//        server.setExecutor(null); // creates a default executor
//        server.start();
//
//
//        // Launch tab or window
//        if (Desktop.isDesktopSupported()) {
//            Desktop.getDesktop().browse(new URI("http://localhost:8000/" + indexName));
//        }
//    }
//
//    private static class MyHandler implements HttpHandler {
//        @Override
//        public void handle(HttpExchange t) throws IOException {
//
//            //test
//            String response2 = readFile("src/html/index.html", Charset.defaultCharset());
//
//            t.sendResponseHeaders(200, response2.length());
//            OutputStream os2 = t.getResponseBody();
//            os2.write(response2.getBytes());
//            os2.close();
//
//
//            String response = readFile("src/html/index.html", Charset.defaultCharset());
//
//            t.sendResponseHeaders(200, response.length());
//            OutputStream os = t.getResponseBody();
//            os.write(response.getBytes());
//            os.close();
//
//
//        }
//    }
//
//    private static String readFile(String path, Charset encoding) throws IOException {
//        byte[] encoded = Files.readAllBytes(Paths.get(path));
//        return new String(encoded, encoding);
//    }
//
//}