from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.utils import platform
import Fruits

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE
    ])

Builder.load_file('interface.kv')

class MyLayout(Widget):

    the_popup = ObjectProperty(None)

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.file_path = selection[0]
        self.the_popup.dismiss()
        print(self.file_path)

        # check for non-empty list i.e. file selected
        if self.file_path:
            self.ids.my_image.source = self.file_path

class FileChoosePopup(Popup):

    load = ObjectProperty()


class HandPoseApp(App):

    def build(self):
        return(MyLayout())

    def classify_image(self):
        img_path = self.root.ids["my_image"].source

        img_features = Fruits.extract_features(img_path)

        predicted_class = Fruits.predict_output("weights.npy", img_features, activation="sigmoid")

        self.root.ids["label"].text = "Predicted Class : " + predicted_class

#firstApp = AwesomeApp(title="Fruits 360 Recognition")
#firstApp.run()

if __name__ == '__main__':
    HandPoseApp().run()
