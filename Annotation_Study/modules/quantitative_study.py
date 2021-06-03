import matplotlib.pyplot as plt

class QuantitativeStudy:

    def __init__(self, jsn:dict) -> None:
        self.metadata = jsn["metadata"]

    def print_metadata(self) -> None:
        print(self.metadata)

    def jaccard_similarity(self, x11:float, x12:float, x21:float, x22:float) -> float:
        I = min(x12, x22) - max(x11, x21)
        U = max(x12, x22) - min(x11, x21)
        return I/U

    def similarity_dict(self) -> dict:
        action:int = 0
        result = {}
        for key1, value in self.metadata.items():
            if action >= len(self.metadata) / 2: break
            # key2 è la chiave che identifica l'etichetta manuale
            key2 = list(key1)
            key2[2] = '2'
            key2 = ''.join(key2)
            result[key1] = {
                "action": value["av"]["1"][:-2],
                "similarity": self.jaccard_similarity(value["z"][0], value["z"][1], self.metadata[key2]["z"][0], self.metadata[key2]["z"][1])
            }
            action += 1
        return result

    def mean(self, similarity:dict, action:bool=False) -> list:
        if not action:
            return [sum(value["similarity"] for value in similarity.values()) / len(similarity)]
        s_take:float = 0
        c_take:float = 0
        s_release:float = 0
        c_release:float = 0
        s_push:float = 0
        c_push:float = 0
        for _, value in similarity.items():
            if value["action"] == "Prendi":
                s_take += value["similarity"]
                c_take += 1
            elif value["action"] == "Rilascia":
                s_release += value["similarity"]
                c_release += 1
            else:
                s_push += value["similarity"]
                c_push += 1
        return [s_take/c_take, s_release/c_release, s_push/c_push]

    def get_similarities(self, similarity:dict) -> list:
        similarities = []
        for _, value in similarity.items():
            similarities.append(value["similarity"])
        return similarities

    def box_plot(self, data:list) -> None:
        green_diamond = dict(markerfacecolor='g', marker='D')
        fig1, ax1 = plt.subplots()
        ax1.set_title('Box Plot')
        ax1.boxplot(data, flierprops=green_diamond)
        if len(data) == 3:
            plt.xticks([1, 2, 3], ['Take', 'Release', 'Push'])
        plt.plot()
    
    def get_similarity_actions(self, similarity:dict) -> list:
        sim_take = []
        sim_release = []
        sim_push = []
        for _, value in similarity.items():
            if value["action"] == "Prendi":
                    sim_take.append(value["similarity"])
            elif value["action"] == "Rilascia":
                sim_release.append(value["similarity"])
            else:
                sim_push.append(value["similarity"])
        return [sim_take, sim_release, sim_push]