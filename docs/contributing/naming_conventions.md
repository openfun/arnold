# Naming conventions

To make created object names the most relevant possible, we defined a set of
naming conventions for Kubernetes objects. The following table sums up those
conventions.

| 0bject type             | Pattern                        | Example            |
| :---------------------- | :----------------------------- | :----------------- |
| volume                  | `{{ service }}-v-{{ name }}`   | `richie-v-media`   |
| persistent volume claim | `{{ service }}-pvc-{{ name }}` | `richie-pvc-media` |
