# 🛍️ API de Pedidos

API destinada ao estudo do FastAPI ! 

## 🗄️ Models

### Tabela: `usuarios`

| Coluna | Tipo | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Identificador único para cada usuário. |
| `email` | String | Unique, Not Null | Endereço de e--mail do usuário. |
| `nome` | String | Not Null | Nome do usuário. |
| `senha` | String | Not Null | Senha do usuário (hash). |
| `ativo` | Boolean | | Indica se o usuário está ativo (padrão `True`). |
| `admin` | Boolean | Default: `False` | Indica se o usuário é um administrador. |

---

### Tabela: `pedidos`

| Coluna | Tipo | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Identificador único para cada pedido. |
| `status` | String | Not Null | Status atual do pedido (ex: "PENDENTE", "FINALIZADO"). |
| `usuario` | Integer | Foreign Key (`usuarios.id`) | ID do usuário que fez o pedido. |
| `preco` | Float | | Preço total do pedido. |

---

### Tabela: `item_Pedido`

| Coluna | Tipo | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Primary Key, Auto Increment | Identificador único para cada item do pedido. |
| `quantidade` | Integer | | Quantidade deste item. |
| `sabor` | String | | Sabor do item (ex: de uma pizza). |
| `tamanho` | String | | Tamanho do item (ex: "Pequeno", "Médio"). |
| `preco_unitario`| Float | | Preço de uma unidade deste item. |
| `pedido` | Integer | Foreign Key (`pedidos.id`) | ID do pedido ao qual este item pertence. |

_*README em construção...*_