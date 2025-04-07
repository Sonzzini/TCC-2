
// Violação múltipla dos princípios SOLID

public class LojaService {

    // SRP: responsabilidade única violada - métodos demais para uma classe só
    public void processarPagamento(String tipoPagamento) {
        if (tipoPagamento.equals("credito")) {
            System.out.println("Processando pagamento com cartão de crédito");
        } else if (tipoPagamento.equals("boleto")) {
            System.out.println("Processando pagamento com boleto.");
        } else {
            System.out.println("Tipo de pagamento inválido");
        }
    }

    public void enviarEmailConfirmacao(String email) {
        System.out.println("Enviando e-mail de confirmação para " + email);
    }

    public void gerarRelatorio() {
        System.out.println("Relatório gerado.");
    }

    // ISP: Interface com métodos desnecessários
    interface Funcionario {
        void vender();
        void limparLoja();
        void fazerRelatorio(); // nem todo funcionário precisa disso
    }

    class Caixa implements Funcionario {
        public void vender() {
            System.out.println("Caixa vendendo...");
        }

        public void limparLoja() {
            // LSP: método que não faz sentido aqui
            throw new UnsupportedOperationException("Caixa não limpa a loja.");
        }

        public void fazerRelatorio() {
            // LSP: idem
            throw new UnsupportedOperationException("Caixa não faz relatório.");
        }
    }

    // DIP: código depende de implementação concreta
    public class ServicoEmail {
        public void enviar(String mensagem) {
            System.out.println("Enviando " + mensagem);
        }
    }

    public void notificarCliente(String mensagem) {
        ServicoEmail email = new ServicoEmail();
        email.enviar(mensagem);
    }
}
