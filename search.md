---
layout: default
title: Arquivos PD Processados
permalink: /search/
---

<div class="publication">
        <div>
        Arquivos PD disponíveis:
        </div>
        <ul>
            {%- for project in site.data -%}
                {%- assign filename_with_extension = project[1].filename -%}
                {%- assign filename_parts = filename_with_extension | split: '.' -%}
                {%- assign filename = filename_parts[0] -%}
                <li><a href="../projetos/{{ filename }}.pd.html">{{ filename }}</a></li>
            {%- endfor -%}
        </ul>
        
    
</div>
