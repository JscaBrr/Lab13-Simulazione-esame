import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def fillDDYear(self):
        for i in self._model.getAllYears():
            self._view._ddAnno.options.append(ft.dropdown.Option(data=i, text=i, on_click=self.readYear))
        self._view.update_page()

    def readYear(self, e):
        self._selectedYear = e.control.data

    def handleCreaGrafo(self,e):
        bool, Nnodes, Nedges, driver = self._model.creaGrafo(self._selectedYear)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Creazione grafo eseguita con successo\nNumero nodi: {Nnodes}\nNumero archi: {Nedges}"))
        self._view.txt_result.controls.append(ft.Text(f"Migliore Driver: {driver[0]}-{driver[1]}"))
        self._view.update_page()

    def handleCerca(self, e):
        sequenza, costo = self._model.calcolaDreamTeam(self._view._txtIntK.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Studio del Dream Team eseguito\nTasso di sconfitta: {costo}\nDream Team:"))
        for i,item in enumerate(sequenza, start=1):
            self._view.txt_result.controls.append(ft.Text(f"{i}. {item}"))
        self._view.update_page()