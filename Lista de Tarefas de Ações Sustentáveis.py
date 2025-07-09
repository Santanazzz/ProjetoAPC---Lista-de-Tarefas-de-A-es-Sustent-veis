import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Lista que armazena as tarefas
tarefas = []

# Sugestões de tarefas sustentáveis
tarefas_sugestao = [
    "Começar a compostar",
    "Usar sacolas reutilizáveis no mercado",
    "Evitar uso de canudos",
    "Apagar luzes ao sair de um cômodo",
    "Separar lixo reciclável",
    "Utilizar transporte público ou bicicleta",
    "Reduzir o tempo no banho",
    "Plantar uma árvore",
    "Levar seu próprio copo para o trabalho",
    "Limpar jarros de plantas"
]

# === Funções ===

# Atualiza visualmente a lista de tarefas na interface
def atualizar_lista():
    lista_tarefas.delete(*lista_tarefas.get_children())  # Limpa a Treeview
    for i, tarefa in enumerate(tarefas):
        status = "✔️" if tarefa["concluida"] else "❌"  # Define o status visual
        cor = "#d4edda" if tarefa["concluida"] else "#fff3cd"  # Cor de fundo por status
        lista_tarefas.insert("", "end", iid=i, values=(f"{i+1}. {tarefa['descricao']}", status), tags=(cor,))

# Adiciona uma nova tarefa à lista
def adicionar_tarefa():
    # Exibe opções de sugestão e permite entrada personalizada
    opcoes = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(tarefas_sugestao))
    escolha = simpledialog.askstring("Nova Tarefa", f"Escolha uma sugestão (1-{len(tarefas_sugestao)}) ou digite a sua:\n\n{opcoes}\n0. Digitar outra tarefa")

    if escolha is None:
        return

    if escolha.isdigit() and 1 <= int(escolha) <= len(tarefas_sugestao):
        descricao = tarefas_sugestao[int(escolha) - 1]
    elif escolha == "0" or not escolha.isdigit():
        descricao = escolha if escolha != "0" else simpledialog.askstring("Tarefa Personalizada", "Digite a descrição da tarefa:")
    else:
        messagebox.showerror("Erro", "Opção inválida.")
        return

    if descricao:
        tarefas.append({"descricao": descricao, "concluida": False})
        if "limpar" in descricao.lower():
            messagebox.showinfo("Boa ação!", "Parabéns pela boa ação de limpeza!")
        atualizar_lista()

# Remove uma tarefa selecionada ou todas, se nenhuma for selecionada
def remover_tarefa():
    selecionado = lista_tarefas.selection()
    if not tarefas:
        messagebox.showinfo("Aviso", "Nenhuma tarefa para remover.")
    elif selecionado:
        idx = int(selecionado[0])
        tarefa = tarefas.pop(idx)
        messagebox.showinfo("Removido", f"Tarefa '{tarefa['descricao']}' removida.")
        atualizar_lista()
    else:
        confirm = messagebox.askyesno("Remover tudo", "Deseja remover TODAS as tarefas?")
        if confirm:
            tarefas.clear()
            atualizar_lista()

# Marca como concluída a tarefa selecionada ou todas, se nenhuma for selecionada
def marcar_concluida():
    selecionado = lista_tarefas.selection()
    if not tarefas:
        messagebox.showinfo("Aviso", "Nenhuma tarefa para marcar.")
    elif selecionado:
        idx = int(selecionado[0])
        tarefas[idx]["concluida"] = True
        messagebox.showinfo("Concluído", "Parabéns, você está tornando o mundo um lugar melhor!")
        atualizar_lista()
    else:
        confirm = messagebox.askyesno("Concluir tudo", "Deseja marcar TODAS como concluídas?")
        if confirm:
            for tarefa in tarefas:
                tarefa["concluida"] = True
            messagebox.showinfo("Tudo concluído!", "Todas as tarefas foram marcadas como concluídas!")
            atualizar_lista()

# === Interface gráfica ===

janela = tk.Tk()
janela.title("🌿 Lista de Tarefas Sustentáveis")
janela.geometry("620x450")
janela.configure(bg="#f0f5f2")  # Cor de fundo

# Título do aplicativo
titulo = tk.Label(janela, text="Tarefas Sustentáveis", font=("Helvetica", 18, "bold"), bg="#f0f5f2", fg="#2f4f4f")
titulo.pack(pady=15)

# Frame que contém a lista com scrollbar
frame_lista = tk.Frame(janela, bg="#f0f5f2")
frame_lista.pack(pady=5)

# Treeview para exibir tarefas e status
lista_tarefas = ttk.Treeview(frame_lista, columns=("Tarefa", "Status"), show="headings", height=12)
lista_tarefas.heading("Tarefa", text="Tarefa")
lista_tarefas.heading("Status", text="Status")
lista_tarefas.column("Tarefa", width=420)
lista_tarefas.column("Status", width=100)

# Scrollbar vertical
scroll = ttk.Scrollbar(frame_lista, orient="vertical", command=lista_tarefas.yview)
lista_tarefas.configure(yscrollcommand=scroll.set)

lista_tarefas.pack(side=tk.LEFT)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Define as cores de fundo das linhas de acordo com a tag
lista_tarefas.tag_configure("#d4edda", background="#d4edda")  # Verde claro para concluídas
lista_tarefas.tag_configure("#fff3cd", background="#fff3cd")  # Amarelo claro para pendentes

# Botões com ações
frame_botoes = tk.Frame(janela, bg="#f0f5f2")
frame_botoes.pack(pady=15)

# Estilo dos botões
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=10)
style.map("TButton", background=[("active", "#b2dfdb")])

# Criação dos botões com ícones
ttk.Button(frame_botoes, text="➕ Adicionar", command=adicionar_tarefa).grid(row=0, column=0, padx=10)
ttk.Button(frame_botoes, text="✅ Concluir", command=marcar_concluida).grid(row=0, column=1, padx=10)
ttk.Button(frame_botoes, text="❌ Remover", command=remover_tarefa).grid(row=0, column=2, padx=10)

# Inicia o loop principal da interface
janela.mainloop()

