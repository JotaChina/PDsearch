---
layout: default
title: Arquivos PD Processados
permalink: /search/
---

<h2>Arquivos PD disponíveis:</h2>

<ul>
{% for project in site.data %}
    {% assign filename_with_extension = project[1].filename %}
    {% assign filename_parts = filename_with_extension | split: '.' %}
    {% assign filename = filename_parts[0] %}
    <li>
        <a href="../../output_pages/{{ filename }}.html">{{ filename }}</a>
    </li>
{% endfor %}
</ul>
