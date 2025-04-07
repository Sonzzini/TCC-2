// Cada classe tem uma única responsabilidade
// Interfaces são específicas
// Dependências são invertidas via abstrações
// Uso de composição em vez de condicionais

// SRP: classe apenas para processar pagamentos
interface MetodoPagamento {
    void processar();
}

// OCP: novo método de pagamento pode ser adicionado sem alterar o código existente
class PagamentoCredito implements MetodoPagamento {
    public void processar() {
        System.out.println("Processando pagamento com cartão de crédito.");
    }
}

class PagamentoBoleto implements MetodoPagamento {
    public void processar() {
        System.out.println("Processando pagamento com boleto.");
    }
}

// SRP: classe apenas para enviar e-mails
class ServicoEmail {
    public void enviarConfirmacao(String email) {
        System.out.println("Enviando e-mail de confirmação para " + email);
    }
}

// ISP: interfaces com métodos específicos por função
interface Vendedor {
    void vender();
}

interface Limpador {
    void limparLoja();
}

class Caixa implements Vendedor {
    public void vender() {
        System.out.println("Caixa vendendo...");
    }
}

// DIP: depende de abstrações, não de implementações concretas
class LojaServiceCorrigido {

    private MetodoPagamento metodoPagamento;
    private ServicoEmail servicoEmail;

    public LojaServiceCorrigido(MetodoPagamento metodoPagamento, ServicoEmail servicoEmail) {
        this.metodoPagamento = metodoPagamento;
        this.servicoEmail = servicoEmail;
    }

    public void realizarVenda(String emailCliente) {
        metodoPagamento.processar();
        servicoEmail.enviarConfirmacao(emailCliente);
    }
}
