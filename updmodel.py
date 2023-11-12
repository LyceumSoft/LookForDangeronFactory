# - НЕ ТРОГАТЬ - #
from roboflow import Roboflow
rf = Roboflow(api_key="6u6b1sk0YqWRx4fQPw3d")
project = rf.workspace().project("presondetext")
model = project.version(1).model
# - НЕ ТРОГАТЬ - #
print(model.predict("F:\!factorysafezoneAI\dataset\\train\images\\0ac92393-35f1-4d67-8bf3-e603b7d28bc8_jpg.rf.5179fa7fca5b4e3fdd888b961896e858.jpg", confidence=40, overlap=30).json())
model.predict("F:\!factorysafezoneAI\dataset\\train\images\\0ac92393-35f1-4d67-8bf3-e603b7d28bc8_jpg.rf.5179fa7fca5b4e3fdd888b961896e858.jpg", confidence=40, overlap=30).save("prediction.jpg")