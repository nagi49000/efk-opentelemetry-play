FROM memgraph/memgraph-mage:1.18.1-memgraph-2.18.1

USER root
# add some handy tools for debug
RUN apt update && \
    apt install -y vim bash && \
    apt clean
# hot fix some code
RUN chmod a+rw /usr/lib/memgraph/query_modules/elastic_search_serialization.py && \
    sed -i 's/from typing import Any, List, Dict, Tuple/from typing import Any, List, Dict, Tuple, Union/g' /usr/lib/memgraph/query_modules/elastic_search_serialization.py && \
    sed -i 's/elastic_url: str, ca_certs: str, elastic_user: str, elastic_password/elastic_url: str, ca_certs: Union[str, None]=None, elastic_user: str="", elastic_password: str=""/g' /usr/lib/memgraph/query_modules/elastic_search_serialization.py && \
    sed -i 's/        hit\[ID\] = hit\[_SOURCE\]\[INDEX\]\[ID\]/        if hit\[_SOURCE\].get(INDEX, None):\n            hit\[ID\] = hit\[_SOURCE\]\[INDEX\]\[ID\]/' /usr/lib/memgraph/query_modules/elastic_search_serialization.py && \
    sed -i 's/        hit\[_SOURCE\].pop(INDEX, None)/            hit\[_SOURCE\].pop(INDEX, None)/' /usr/lib/memgraph/query_modules/elastic_search_serialization.py && \
    sed -i 's/        item\[ID\] = item\[_SOURCE\]\[INDEX\]\[ID\]/        if item\[_SOURCE\].get(INDEX, None):\n            item\[ID\] = item\[_SOURCE\]\[INDEX\]\[ID\]/' /usr/lib/memgraph/query_modules/elastic_search_serialization.py && \
    sed -i 's/        item\[_SOURCE\].pop(INDEX, None)/            item\[_SOURCE\].pop(INDEX, None)/' /usr/lib/memgraph/query_modules/elastic_search_serialization.py
USER memgraph