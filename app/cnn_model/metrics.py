import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

from app.cnn_model.model import model
from app.cnn_model.train_model import X_val, Y_val


def plot_sample(X, Y, Y_pred, idx, ax, image_names=None, title=""):
    ax.imshow(X[idx])
    if image_names:
        img_title = f"Predicted: {Y_pred[idx]}, Actual: {Y[idx]}\nName: {image_names[idx]}\n{title}"
    else:
        img_title = f"Predicted: {Y_pred[idx]}, Actual: {Y[idx]}\n{title}"
    ax.set_title(img_title)
    ax.axis('off')


# Predict the values from the validation dataset
Y_pred = model.predict(X_val)
# Convert predictions classes to one hot vectors
Y_pred_classes = np.argmax(Y_pred, axis=1)
# Convert validation observations to one hot vectors
Y_true = np.argmax(Y_val, axis=1)
# compute the confusion matrix

accuracy = accuracy_score(Y_true, Y_pred_classes)
print("Accuracy:", accuracy)

cm = confusion_matrix(Y_true, Y_pred_classes)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()

# Find indices of different cases
true_positive = np.where((Y_pred_classes == 1) & (Y_true == 1))[0]
false_positive = np.where((Y_pred_classes == 1) & (Y_true == 0))[0]
false_negative = np.where((Y_pred_classes == 0) & (Y_true == 1))[0]
true_negative = np.where((Y_pred_classes == 0) & (Y_true == 0))[0]

# Randomly choose one sample from each case
tp_sample = np.random.choice(true_positive)
fp_sample = np.random.choice(false_positive)
fn_sample = np.random.choice(false_negative)
tn_sample = np.random.choice(true_negative)

# Plotting
fig, axes = plt.subplots(2, 2, figsize=(10, 10))  # 2x2 grid for all cases

# Plotting True Positive
plot_sample(X_val, Y_true, Y_pred_classes, tp_sample, axes[0, 0], None, "True Positive")
# Plotting False Positive
plot_sample(X_val, Y_true, Y_pred_classes, fp_sample, axes[0, 1], None, "False Positive")

# Plotting False Negative
plot_sample(X_val, Y_true, Y_pred_classes, fn_sample, axes[1, 0], None, "False Negative")

# Plotting True Negative
plot_sample(X_val, Y_true, Y_pred_classes, tn_sample, axes[1, 1], None, "True Negative")

plt.show()

precision = precision_score(Y_true, Y_pred_classes)
recall = recall_score(Y_true, Y_pred_classes)
f1 = f1_score(Y_true, Y_pred_classes)

print("Precision:", precision)
print("Recall:", recall)
print("F1-Score:", f1)
