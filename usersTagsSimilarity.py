import crawler
import json
import matplotlib.pyplot as plt
import numpy
import userIllustsTagsAnalysis
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

"""Using dimension reduction algorithms (PCA and t-SNE) to visualize similarity between artists."""

def main(uids):
    user_names = []
    user_illust_count = []
    pids = []
    for uid in uids:
        user_names.append(userIllustsTagsAnalysis.get_user_name(uid=uid))
        user_pid = userIllustsTagsAnalysis.get_user_illusts(uid)
        user_illust_count.append(len(user_pid))
        for pid in user_pid:
            pids.append(pid)

    print(user_names)
    print(user_illust_count)
    print(pids)
    print(len(pids))

    all_tags = []
    pids_tags = {}
    count = 0
    for pid in pids:
        raw_text = crawler.illusts_text(pid=pid)
        parsed_text = json.loads(raw_text)
        tags = parsed_text["body"][pid]["tags"]
        pids_tags[pid] = tags

        for tag in tags:
            if tag not in all_tags:
                all_tags.append(tag)

        count += 1
        print(str(count) + " / " + str(len(pids)))

    print(pids_tags)
    print(all_tags)

    pid_tag_array = numpy.zeros((len(pids), len(all_tags)))
    id_count = 0
    for item in pids_tags.items():
        tag_count = 0
        for tag in all_tags:
            if tag in item[1]:
                pid_tag_array[id_count, tag_count] = 1
            tag_count += 1
        print(item)
        id_count += 1
    print(pid_tag_array)

    pca = PCA(n_components=2)
    reduced_array = pca.fit_transform(pid_tag_array)
    print(reduced_array)

    reduced_array_list = []
    start = 0
    end = 0
    for i in range(len(uids)):
        end = end + user_illust_count[i]
        reduced_array_list.append(reduced_array[start:end])
        start = end

    plt.subplot(1, 2, 1)
    colors = "bgrcmykw"
    color_index = 0
    handles = []
    for group in reduced_array_list:
        for X, Y in group:
            handles.append(plt.scatter(X, Y, c=colors[color_index]))
        color_index += 1

    # add figure legend
    for i in range(len(reduced_array_list)):
        plt.scatter([], [], c=list(colors)[i], s=100, label=user_names[i])
    plt.legend(frameon=False)

    ts = TSNE(n_components=2, init='pca', random_state=0)
    reduced_array = ts.fit_transform(pid_tag_array)

    reduced_array_list = []
    start = 0
    end = 0
    for i in range(len(uids)):
        end = end + user_illust_count[i]
        reduced_array_list.append(reduced_array[start:end])
        start = end

    plt.subplot(1, 2, 2)
    colors = "bgrcmykw"
    color_index = 0
    handles = []
    for group in reduced_array_list:
        for X, Y in group:
            handles.append(plt.scatter(X, Y, c=colors[color_index]))
        color_index += 1

    # add figure legend
    for i in range(len(reduced_array_list)):
        plt.scatter([], [], c=list(colors)[i], s=100, label=user_names[i])
    plt.legend(frameon=False)

    plt.show()


if __name__ == "__main__":
    #main(uids=[3104565, 27350443, 212801, 341818, 1980643, 4462245])
    main(uids=[3104565, 1980643, 4462245])
