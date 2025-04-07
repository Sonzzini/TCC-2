public class App {
    public static void main(String[] args) throws Exception {
        LojaService loja = new LojaService();
        loja.processarPagamento("credito");

        MetodoPagamento pagamento = new PagamentoCredito(); // Pode ser trocado
        ServicoEmail email = new ServicoEmail();
        LojaServiceCorrigido lojaCorrigida = new LojaServiceCorrigido(pagamento, email);

        lojaCorrigida.realizarVenda("cliente@email.com");
    }
}
