import matplotlib.pyplot as plt
import numpy as np


plt.figure(1, figsize=(8,4))
x = np.arange(3)
errors = [0.4690, 0.0640, 0.0543]
plt.bar(x, errors, color='orange')
plt.title('Error comparison')
plt.ylabel('Error')
plt.xticks(x, ['FFN','CNN','LSTM'], rotation=60)
for i, v in enumerate(errors):
    plt.text(i-0.12,v-0.03, '%.3f' % v, color='black',fontweight='bold')
plt.show()

plt.figure(2, figsize=(8,4))
x = np.arange(3)
accuracy = [0.7775, 0.9717, 0.9875]
plt.bar(x, accuracy, color='yellow')
plt.title('Accuracy comparison')
plt.ylabel('Accuracy')
plt.xticks(x, ['FFN','CNN','LSTM'], rotation=60)
for i, v in enumerate(accuracy):
    plt.text(i-0.12,v-0.06, '%.3f' % v, color='black',fontweight='bold')
plt.show()