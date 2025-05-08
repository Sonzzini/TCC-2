import java.time.LocalDateTime;

public class LoggerManager {
    public static void log(String message) {
        System.out.println("[" + LocalDateTime.now() + "] " + message);
    }
}
