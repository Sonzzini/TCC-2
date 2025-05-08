public class ViewModel {

    private final DataManagerInterface dataManager;
    private final NetworkManagerInterface networkManager;

    public ViewModel(DataManagerInterface dataManager, NetworkManagerInterface networkManager) {
        // Constructor for ViewModel
        this.dataManager = dataManager;
        this.networkManager = networkManager;
        LoggerManager.log("ViewModel initialized");
    }

    public String getData() {
        // Fetch data from DataManagerInterface
        return dataManager.fetchData();
    }

    public String getNetworkData() {
        // Fetch data from NetworkManager
        return networkManager.fetchDataFromNetwork();
    }

    public void saveData(String data) {
        // Save data using DataManagerInterface
        dataManager.saveData(data);
    }

    public void sendData(String data) {
        // Send data using NetworkManager
        networkManager.sendDataToNetwork(data);
    }
}
