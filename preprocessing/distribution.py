import numpy as np

# Bilang ng images sa bawat set
train_counts = np.array([84, 91, 99, 74, 89, 70, 91, 82, 70, 88, 81, 99, 103, 91, 75, 91, 98, 70, 84, 81, 84, 77, 91, 70, 77, 77, 91, 91, 119, 70, 77, 86, 99, 91, 102, 96, 77, 91, 98, 98])
val_counts = np.array([18, 19, 21, 15, 19, 15, 19, 17, 15, 18, 17, 21, 22, 19, 16, 19, 21, 15, 18, 17, 18, 16, 19, 15, 16, 16, 19, 19, 25, 15, 16, 18, 21, 19, 21, 20, 16, 19, 21, 21])
test_counts = np.array([18, 20, 22, 17, 20, 15, 20, 19, 15, 20, 18, 22, 23, 20, 17, 20, 21, 15, 18, 18, 18, 17, 20, 15, 17, 17, 20, 20, 27, 15, 17, 20, 22, 20, 23, 22, 17, 20, 21, 21])

# Kabuuang bilang ng images per class
total_counts = train_counts + val_counts + test_counts

# Compute correct percentages per class
train_percentage = (train_counts / total_counts) * 100
val_percentage = (val_counts / total_counts) * 100
test_percentage = (test_counts / total_counts) * 100

# Print results
for i, (train, val, test) in enumerate(zip(train_percentage, val_percentage, test_percentage), 1):
    print(f"Class {i}: Train {train:.2f}%, Val {val:.2f}%, Test {test:.2f}%")

# Check overall dataset split (should be close to your intended split, e.g., 70-15-15)
total_train = train_counts.sum()
total_val = val_counts.sum()
total_test = test_counts.sum()
total_dataset = total_train + total_val + total_test

print("\nDataset Distribution:")
print(f"Total Train: {total_train / total_dataset * 100:.2f}%")
print(f"Total Validation: {total_val / total_dataset * 100:.2f}%")
print(f"Total Test: {total_test / total_dataset * 100:.2f}%")
