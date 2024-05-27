from abc import abstractmethod

from gi.repository import Gtk

from tlpui import language


class AppPage:
    name: str

    def append_to_notebook(self, notebook: Gtk.Notebook):
        # stat_page = StatisticsPage()
        stat_box = self.create_box()
        stat_label = Gtk.Label(language.MT_(self.name))
        stat_label.set_hexpand(True)
        notebook.append_page(stat_box, stat_label)

    @abstractmethod
    def create_box(self):
        pass
