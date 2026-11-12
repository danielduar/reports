<template>
  <div :class="{ 'dark': isDark }" class="min-h-screen transition-colors duration-200">
    <div class="bg-slate-100 dark:bg-slate-950 text-slate-900 dark:text-slate-100 min-h-screen p-3 sm:p-5 text-xs sm:text-[8.5pt]">
      <div class="max-w-7xl mx-auto">

        <!-- Top Header -->
        <header class="bg-white dark:bg-slate-900 p-4 sm:p-5 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 mb-4 transition-colors">
          <div class="flex flex-wrap justify-between items-center gap-3">
            <div>
              <div class="flex items-center gap-2">
                <span class="inline-block w-2.5 h-2.5 rounded-full bg-indigo-600 dark:bg-indigo-400 animate-pulse print:hidden"></span>
                <h1 class="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
                  Gestão de Relatórios
                </h1>
                <span class="text-[7.5pt] font-semibold uppercase px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-950/70 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800">
                  Vue 3 + DB
                </span>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                Ano Teocrático: <strong class="text-slate-700 dark:text-slate-200">{{ selectedServiceYear }}</strong> •
                Mês: <strong class="text-slate-700 dark:text-slate-200">{{ selectedMonth === 'all' ? 'Todos os Meses' : selectedMonth }}</strong>
              </p>
            </div>

            <!-- Header Controls -->
            <div class="flex items-center gap-2 flex-wrap no-print">
              <!-- DB Connection Badge -->
              <span :class="dbConnected ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300 border-emerald-300 dark:border-emerald-700' : 'bg-amber-100 text-amber-800 dark:bg-amber-950/80 dark:text-amber-300 border-amber-300 dark:border-amber-700'" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[7.5pt] font-semibold border transition-colors shadow-2xs">
                <span :class="dbConnected ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'" class="w-2 h-2 rounded-full"></span>
                {{ dbConnected ? 'Banco Conectado' : 'Modo Offline / Local' }}
              </span>

              <!-- Feedback Toast de Salvamento -->
              <transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0 translate-y-1" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
                <span v-if="saveSuccessMessage" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[7.5pt] font-bold bg-emerald-600 text-white shadow-sm">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                  {{ saveSuccessMessage }}
                </span>
              </transition>

              <!-- Botões de Backup / Restaurar -->
              <button @click="exportBackup" type="button" class="inline-flex items-center gap-1 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 px-2.5 py-1.5 rounded-lg text-xs font-medium transition shadow-2xs" title="Baixar backup dos relatórios">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                <span>Backup</span>
              </button>
              <label class="inline-flex items-center gap-1 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 px-2.5 py-1.5 rounded-lg text-xs font-medium transition shadow-2xs cursor-pointer" title="Restaurar backup">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l4-4m0 0l4 4m-4-4v12"/></svg>
                <span>Restaurar</span>
                <input type="file" accept=".json" @change="importBackup" class="hidden">
              </label>

              <!-- Dark Mode Toggle -->
              <button @click="toggleDarkMode" type="button" class="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 transition-colors shadow-2xs" title="Alternar tema">
                <svg v-if="isDark" class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <svg v-else class="w-4 h-4 text-slate-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              </button>

              <!-- Botão Lançar Relatório -->
              <button @click="openReportModal()" class="inline-flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 text-white px-3.5 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                </svg>
                <span>Lançar Relatório</span>
              </button>

              <!-- Botão Imprimir Fichas em Lote -->
              <button @click="printAllPublishersCardsPDF" class="inline-flex items-center gap-1.5 bg-indigo-700 hover:bg-indigo-800 text-white px-3.5 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition" title="Gerar PDF com ficha de todos">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <span>Fichas de Todos (PDF)</span>
              </button>
            </div>
          </div>

          <!-- Abas de Navegação -->
          <div class="flex items-center gap-2 mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 no-print overflow-x-auto">
            <button @click="currentTab = 'reports'" :class="currentTab === 'reports' ? 'bg-indigo-600 text-white shadow-xs' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'" class="px-3.5 py-1.5 rounded-lg font-semibold text-xs transition whitespace-nowrap">
              Relatórios Entregues ({{ deliveredReports.length }})
            </button>
            <button @click="currentTab = 'pending'" :class="currentTab === 'pending' ? 'bg-amber-600 text-white shadow-xs' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'" class="px-3.5 py-1.5 rounded-lg font-semibold text-xs transition whitespace-nowrap">
              Faltam Entregar ({{ pendingPublishers.length }})
            </button>
            <button @click="currentTab = 'publishers'" :class="currentTab === 'publishers' ? 'bg-slate-800 dark:bg-slate-700 text-white shadow-xs' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'" class="px-3.5 py-1.5 rounded-lg font-semibold text-xs transition whitespace-nowrap">
              Irmãos Cadastrados ({{ activePublishers.length }})
            </button>
            <button @click="currentTab = 'groups'" :class="currentTab === 'groups' ? 'bg-emerald-700 text-white shadow-xs' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'" class="px-3.5 py-1.5 rounded-lg font-semibold text-xs transition whitespace-nowrap">
              Gestão de Grupos ({{ groups.length }})
            </button>
          </div>
        </header>

        <!-- Cards de Resumo Analítico -->
        <section class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-4">
          <div class="bg-white dark:bg-slate-900 p-3 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
            <span class="text-[7pt] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 block">Total de Horas</span>
            <span class="text-lg font-bold text-slate-900 dark:text-white mt-0.5 block">{{ stats.totalHours }} h</span>
            <span class="text-[7pt] text-slate-400">Média: {{ stats.avgHours }} h</span>
          </div>
          <div class="bg-white dark:bg-slate-900 p-3 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
            <span class="text-[7pt] font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400 block">Trabalharam</span>
            <span class="text-lg font-bold text-emerald-700 dark:text-emerald-300 mt-0.5 block">{{ stats.worked }}</span>
            <span class="text-[7pt] text-emerald-600/70">No campo</span>
          </div>
          <div class="bg-white dark:bg-slate-900 p-3 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
            <span class="text-[7pt] font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400 block">Faltam Entregar</span>
            <span class="text-lg font-bold text-rose-700 dark:text-rose-400 mt-0.5 block">{{ pendingPublishers.length }}</span>
            <span class="text-[7pt] text-rose-500/80">Cobrança ativa</span>
          </div>
          <div class="bg-white dark:bg-slate-900 p-3 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
            <span class="text-[7pt] font-bold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 block">Estudos Bíblicos</span>
            <span class="text-lg font-bold text-indigo-700 dark:text-indigo-300 mt-0.5 block">{{ stats.studies }}</span>
            <span class="text-[7pt] text-indigo-500/80">Total relatado</span>
          </div>
          <div class="bg-white dark:bg-slate-900 p-3 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
            <span class="text-[7pt] font-bold uppercase tracking-wider text-purple-600 dark:text-purple-400 block">Pioneiros</span>
            <div class="flex items-center gap-2 mt-0.5">
              <span class="text-xs font-bold text-purple-700 dark:text-purple-300">{{ stats.pr }} PR</span>
              <span class="text-xs text-slate-400">•</span>
              <span class="text-xs font-bold text-purple-700 dark:text-purple-300">{{ stats.pa }} PA</span>
            </div>
            <span class="text-[7pt] text-purple-500/80">Regulares e Auxiliares</span>
          </div>
          <div class="bg-white dark:bg-slate-900 p-3 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
            <span class="text-[7pt] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400 block">Publicadores</span>
            <div class="flex items-center gap-2 mt-0.5">
              <span class="text-xs font-bold text-blue-700 dark:text-blue-300">{{ stats.pb }} PB</span>
              <span class="text-xs text-slate-400">•</span>
              <span class="text-xs font-bold text-blue-700 dark:text-blue-300">{{ stats.pnb }} PNB</span>
            </div>
            <span class="text-[7pt] text-blue-500/80">Batizados e Não Batizados</span>
          </div>
        </section>

        <!-- Barra de Filtros Reativos -->
        <section class="bg-white dark:bg-slate-900 p-3.5 sm:p-4 rounded-xl border border-slate-200 dark:border-slate-800 mb-4 shadow-2xs no-print">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
            <div>
              <label class="block text-[7pt] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Ano de Serviço</label>
              <select v-model="selectedServiceYear" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 font-medium text-slate-800 dark:text-slate-100">
                <option v-for="yr in availableServiceYears" :key="yr" :value="yr">{{ yr }}</option>
              </select>
            </div>
            <div>
              <label class="block text-[7pt] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Mês de Referência</label>
              <div class="flex items-center gap-1">
                <select v-model="selectedMonth" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                  <option value="all">Todos os Meses</option>
                  <option v-for="(m, idx) in theocraticMonths" :key="m" :value="m">{{ idx + 1 }}. {{ m }}</option>
                </select>
                <button @click="resetToCurrentMonth" title="Ir para o mês teocrático de cobrança atual" class="p-1.5 bg-slate-100 dark:bg-slate-800 hover:bg-indigo-50 dark:hover:bg-indigo-900/40 text-slate-600 dark:text-slate-300 rounded-lg transition">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </button>
              </div>
            </div>
            <div>
              <label class="block text-[7pt] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Grupo de Serviço</label>
              <select v-model="selectedGroup" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                <option value="all">Todos os Grupos</option>
                <option v-for="g in groupNames" :key="g" :value="g">{{ g }}</option>
              </select>
            </div>
            <div>
              <label class="block text-[7pt] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Privilégio</label>
              <select v-model="selectedPrivilege" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                <option value="all">Todos os Privilégios</option>
                <option value="PR">Pioneiros Regulares (PR)</option>
                <option value="PA">Pioneiros Auxiliares (PA)</option>
                <option value="PB">Publicadores Batizados (PB)</option>
                <option value="PNB">Pub. Não Batizados (PNB)</option>
              </select>
            </div>
            <div>
              <label class="block text-[7pt] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1">Buscar Irmão</label>
              <div class="relative">
                <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Filtrar por nome..."
                    class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg pl-8 pr-2.5 py-1.5 text-slate-800 dark:text-slate-100"
                />
                <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>
          </div>
        </section>

        <!-- ABA 1: RELATÓRIOS ENTREGUES -->
        <main v-if="currentTab === 'reports'" class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs overflow-hidden">
          <div class="p-4 border-b border-slate-100 dark:border-slate-800 flex justify-between items-center gap-3 flex-wrap">
            <div>
              <h2 class="font-bold text-sm text-slate-900 dark:text-white">Relação Analítica de Relatórios Entregues</h2>
              <p class="text-[7.5pt] text-slate-500 dark:text-slate-400">Exibindo {{ filteredReports.length }} relatórios entregues</p>
            </div>
            <div class="flex items-center gap-2 flex-wrap no-print">
              <button @click="triggerPrint" class="inline-flex items-center gap-1.5 bg-slate-800 hover:bg-slate-900 text-white dark:bg-slate-700 dark:hover:bg-slate-600 px-3 py-1.5 rounded-lg text-xs font-semibold shadow-2xs transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 9V2h12v7M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2m-12 0v4h12v-4m-12 0h12" /></svg>
                <span>Imprimir Lista Geral</span>
              </button>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-[8.5pt]">
              <thead>
              <tr class="bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-semibold">
                <th class="py-2.5 px-3 w-10 text-center">#</th>
                <th class="py-2.5 px-3">Publicador</th>
                <th class="py-2.5 px-2.5 w-24 text-center">Grupo</th>
                <th class="py-2.5 px-2.5 w-28 text-center">Mês/Ano</th>
                <th class="py-2.5 px-3 w-36">Privilégio</th>
                <th class="py-2.5 px-2 text-center w-16">Horas</th>
                <th class="py-2.5 px-2 text-center w-16">Estudos</th>
                <th class="py-2.5 px-2 text-center w-20">Trabalhou</th>
                <th class="py-2.5 px-3">Observações</th>
                <th class="py-2.5 px-3 w-36 text-center no-print">Ações</th>
              </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-800 text-slate-800 dark:text-slate-200">
              <tr v-for="(rep, idx) in paginatedReports" :key="rep.id || rep.name + rep.month" class="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition">
                <td class="py-2 px-3 text-center text-slate-400 font-medium">{{ reportsStartIndex + idx + 1 }}</td>
                <td class="py-2 px-3 font-semibold text-slate-900 dark:text-white">
                  <div class="flex items-center gap-1.5 flex-wrap">
                    <span>{{ rep.name }}</span>
                    <span v-if="getPioneerNumber(rep.name)" class="inline-flex items-center px-1.5 py-0.2 text-[6.5pt] font-extrabold uppercase rounded-full bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300 border border-purple-300 dark:border-purple-800" :title="'Pioneiro Regular #' + getPioneerNumber(rep.name)">
                        PR #{{ getPioneerNumber(rep.name) }}
                      </span>
                  </div>
                </td>
                <td class="py-2 px-2.5 text-center">
                  <span class="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 px-2 py-0.5 rounded text-[7.5pt] font-semibold">{{ rep.group }}</span>
                </td>
                <td class="py-2 px-2.5 text-center text-slate-600 dark:text-slate-400">{{ rep.month }} ({{ rep.service_year || selectedServiceYear }})</td>
                <td class="py-2 px-3">
                    <span :class="getPrivilegeBadgeClass(rep.privilege)" class="inline-block px-2 py-0.5 rounded text-[7.5pt] font-semibold">
                      {{ rep.privilege }}
                    </span>
                </td>
                <td class="py-2 px-2 text-center font-bold" :class="repHoursClass(rep.hours)">{{ rep.hours }} h</td>
                <td class="py-2 px-2 text-center font-semibold text-indigo-600 dark:text-indigo-400">{{ rep.estudos }}</td>
                <td class="py-2 px-2 text-center">
                    <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[7pt] font-bold bg-emerald-100 dark:bg-emerald-950/70 text-emerald-800 dark:text-emerald-300">
                      {{ rep.worked || 'Sim' }}
                    </span>
                </td>
                <td class="py-2 px-3 text-slate-600 dark:text-slate-400 italic text-[8pt]">{{ rep.obs || '—' }}</td>
                <td class="py-2 px-3 text-center no-print">
                  <div class="inline-flex items-center gap-1.5">
                    <button @click="editReport(rep)" class="p-1 text-slate-500 hover:text-indigo-600 dark:text-slate-400 dark:hover:text-indigo-300 rounded transition" title="Editar este relatório">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                    </button>
                    <button @click="printPublisherCard(rep.name)" class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-indigo-50 dark:bg-indigo-950/60 hover:bg-indigo-100 dark:hover:bg-indigo-900 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 text-[7.5pt] font-semibold shadow-2xs transition" title="Gerar Ficha/Relatório em PDF deste irmão">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                      <span>PDF</span>
                    </button>
                    <!-- Botão de Excluir Relatório -->
                    <button @click="confirmDeleteReport(rep)" class="p-1 text-slate-400 hover:text-rose-600 dark:hover:text-rose-400 rounded transition" title="Excluir este relatório">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredReports.length === 0">
                <td colspan="10" class="py-8 text-center text-slate-400 italic">
                  Nenhum relatório encontrado para os filtros selecionados.
                </td>
              </tr>
              </tbody>
            </table>
          </div>

          <!-- Controles de Paginação: Relatórios -->
          <div v-if="filteredReports.length > 0" class="p-3 border-t border-slate-100 dark:border-slate-800 flex flex-wrap justify-between items-center gap-3 text-xs no-print bg-slate-50/60 dark:bg-slate-900/60">
            <div class="flex items-center gap-2">
              <span class="text-slate-500 dark:text-slate-400 text-[8pt]">Itens por página:</span>
              <select v-model.number="reportsPerPage" class="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-200 rounded-md px-2 py-1 text-[8pt]">
                <option :value="10">10</option>
                <option :value="20">20</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
                <option :value="9999">Todos</option>
              </select>
              <span class="text-slate-500 dark:text-slate-400 text-[8pt]">
                Mostrando {{ reportsStartIndex + 1 }} - {{ Math.min(reportsStartIndex + reportsPerPage, filteredReports.length) }} de {{ filteredReports.length }}
              </span>
            </div>

            <div class="flex items-center gap-1.5">
              <button
                  @click="reportsCurrentPage = 1"
                  :disabled="reportsCurrentPage <= 1"
                  class="px-2 py-1 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-100 dark:hover:bg-slate-700 font-semibold transition"
                  title="Primeira página"
              >&laquo;</button>
              <button
                  @click="reportsCurrentPage--"
                  :disabled="reportsCurrentPage <= 1"
                  class="px-2.5 py-1 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-100 dark:hover:bg-slate-700 font-semibold transition"
                  title="Página anterior"
              >&lsaquo; Anterior</button>

              <span class="px-2.5 py-1 text-[8pt] font-semibold text-slate-700 dark:text-slate-300">
                Pág. {{ reportsCurrentPage }} de {{ reportsTotalPages }}
              </span>

              <button
                  @click="reportsCurrentPage++"
                  :disabled="reportsCurrentPage >= reportsTotalPages"
                  class="px-2.5 py-1 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-100 dark:hover:bg-slate-700 font-semibold transition"
                  title="Próxima página"
              >Próxima &rsaquo;</button>
              <button
                  @click="reportsCurrentPage = reportsTotalPages"
                  :disabled="reportsCurrentPage >= reportsTotalPages"
                  class="px-2 py-1 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-100 dark:hover:bg-slate-700 font-semibold transition"
                  title="Última página"
              >&raquo;</button>
            </div>
          </div>
        </main>

        <!-- ABA 2: FALTAM ENTREGAR (PENDÊNCIAS POR GRUPO) -->
        <main v-if="currentTab === 'pending'" class="space-y-4">
          <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 flex flex-wrap justify-between items-center gap-3 no-print">
            <div>
              <h2 class="font-bold text-sm text-slate-900 dark:text-white">Acompanhamento de Entregas por Grupo</h2>
              <p class="text-[7.5pt] text-slate-500 dark:text-slate-400">Total de {{ pendingPublishers.length }} publicadores com relatório pendente</p>
            </div>
            <div class="flex items-center gap-2">
              <button @click="printPendingListPDF" class="inline-flex items-center gap-1.5 bg-amber-600 hover:bg-amber-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 9V2h12v7M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2m-12 0v4h12v-4m-12 0h12" />
                </svg>
                <span>Gerar PDF Pendentes</span>
              </button>
              <button @click="copyWhatsAppPendingText" class="inline-flex items-center gap-1.5 bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                </svg>
                <span>Copiar p/ WhatsApp</span>
              </button>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
            <div v-for="g in groupNames" :key="g" :class="groupPending(g).length === 0 ? 'border-emerald-300 bg-emerald-50/40 dark:border-emerald-800 dark:bg-emerald-950/20' : 'border-amber-200 dark:border-amber-900/60 bg-white dark:bg-slate-900'" class="border rounded-xl p-3.5 shadow-2xs transition-colors">
              <div class="flex justify-between items-center px-2.5 py-1.5 rounded-lg mb-2" :class="groupPending(g).length === 0 ? 'bg-emerald-100 dark:bg-emerald-900/40 text-emerald-900 dark:text-emerald-300' : 'bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200'">
                <span class="font-bold text-xs">{{ g }}</span>
                <span class="text-[7.5pt] font-bold px-2 py-0.5 rounded-full" :class="groupPending(g).length === 0 ? 'bg-emerald-200 dark:bg-emerald-800 text-emerald-900 dark:text-emerald-100' : 'bg-amber-100 dark:bg-amber-950 text-amber-900 dark:text-amber-300'">
                  {{ groupPending(g).length === 0 ? '100% Entregue' : groupPending(g).length + ' pendentes' }}
                </span>
              </div>

              <div v-if="groupPending(g).length === 0" class="text-center py-6 text-emerald-600 dark:text-emerald-400">
                <svg class="w-7 h-7 mx-auto mb-1 text-emerald-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <p class="font-bold text-xs">Todos os relatórios entregues!</p>
              </div>

              <ol v-else class="list-decimal ml-4 space-y-1.5 text-[8pt] text-slate-700 dark:text-slate-300">
                <li v-for="pub in groupPending(g)" :key="pub.name" class="flex justify-between items-center group py-0.5">
                  <span class="font-medium pr-1 flex items-center gap-1.5 flex-wrap">
                    <span>{{ pub.name }}</span>
                    <span v-if="getPioneerNumber(pub.name)" class="inline-flex items-center px-1.5 py-0.2 text-[6.5pt] font-extrabold uppercase rounded-full bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300 border border-purple-300 dark:border-purple-800">
                      PR #{{ getPioneerNumber(pub.name) }}
                    </span>
                  </span>
                  <div class="flex items-center gap-1.5 no-print">
                    <button @click="printPublisherCard(pub.name)" class="text-[7pt] bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 px-1.5 py-0.5 rounded border border-slate-300 dark:border-slate-700 transition" title="Ver ficha teocrática completa em PDF">
                      Relatório PDF
                    </button>
                    <button @click="quickReport(pub)" class="text-[7pt] bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-950/60 dark:hover:bg-indigo-900 text-indigo-700 dark:text-indigo-300 px-2 py-0.5 rounded border border-indigo-200 dark:border-indigo-800 font-semibold transition">
                      Lançar
                    </button>
                  </div>
                </li>
              </ol>
            </div>
          </div>
        </main>

        <!-- ABA 3: CADASTRO DE IRMÃOS (ROSTER GERAL) -->
        <main v-if="currentTab === 'publishers'" class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs overflow-hidden">
          <div class="p-4 border-b border-slate-100 dark:border-slate-800 flex justify-between items-center gap-3 flex-wrap">
            <div>
              <h2 class="font-bold text-sm text-slate-900 dark:text-white">Relação Geral de Publicadores Cadastrados</h2>
              <p class="text-[7.5pt] text-slate-500 dark:text-slate-400">Total de {{ activePublishers.length }} publicadores ativos (Incluindo Heitor no G6)</p>
            </div>
            <div class="flex items-center gap-2 flex-wrap no-print">
              <button @click="printAllPublishersCardsPDF" class="inline-flex items-center gap-1.5 bg-indigo-50 dark:bg-indigo-950/70 hover:bg-indigo-100 dark:hover:bg-indigo-900 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 px-3 py-1.5 rounded-lg text-xs font-semibold shadow-2xs transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
                <span>Imprimir Fichas em Lote</span>
              </button>
              <button @click="openPublisherModal()" class="inline-flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-sm transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" /></svg>
                <span>Cadastrar Novo Irmão</span>
              </button>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-[8.5pt]">
              <thead>
              <tr class="bg-slate-50 dark:bg-slate-800/60 border-b border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-semibold">
                <th class="py-2.5 px-3 w-10 text-center">#</th>
                <th class="py-2.5 px-3">Nome do Publicador</th>
                <th class="py-2.5 px-2.5 w-20 text-center">Gênero</th>
                <th class="py-2.5 px-2.5 w-24 text-center">Grupo</th>
                <th class="py-2.5 px-3 w-32">Privilégio</th>
                <th class="py-2.5 px-3 w-28 text-center">Esperança</th>
                <th class="py-2.5 px-2.5 w-24 text-center">Nascimento</th>
                <th class="py-2.5 px-2.5 w-24 text-center">Batismo</th>
                <th class="py-2.5 px-2 text-center w-20">Status</th>
                <th class="py-2.5 px-3">Observações</th>
                <th class="py-2.5 px-3 w-32 text-center no-print">Ações</th>
              </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-800 text-slate-800 dark:text-slate-200">
              <tr v-for="(pub, idx) in paginatedPublishers" :key="pub.name" class="hover:bg-slate-50/80 dark:hover:bg-slate-800/50 transition">
                <td class="py-2 px-3 text-center text-slate-400 font-medium">{{ publishersStartIndex + idx + 1 }}</td>
                <td class="py-2 px-3 font-semibold text-slate-900 dark:text-white">
                  <div class="flex items-center gap-1.5 flex-wrap">
                    <span>{{ pub.name }}</span>
                    <span v-if="getPioneerNumber(pub.name)" class="inline-flex items-center px-1.5 py-0.2 text-[6.5pt] font-extrabold uppercase rounded-full bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300 border border-purple-300 dark:border-purple-800" :title="'Pioneiro Regular #' + getPioneerNumber(pub.name)">
                        PR #{{ getPioneerNumber(pub.name) }}
                      </span>
                  </div>
                </td>
                <td class="py-2 px-2.5 text-center">
                    <span :class="pub.gender === 'Feminino' ? 'bg-pink-100 text-pink-700 dark:bg-pink-950/70 dark:text-pink-300' : 'bg-blue-100 text-blue-700 dark:bg-blue-950/70 dark:text-blue-300'" class="px-2 py-0.5 rounded text-[7pt] font-semibold">
                      {{ pub.gender || 'Masculino' }}
                    </span>
                </td>
                <td class="py-2 px-2.5 text-center">
                  <span class="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 px-2 py-0.5 rounded text-[7.5pt] font-semibold">{{ pub.group }}</span>
                </td>
                <td class="py-2 px-3">
                    <span :class="getPrivilegeBadgeClass(pub.defaultPriv)" class="inline-block px-2 py-0.5 rounded text-[7.5pt] font-semibold">
                      {{ pub.defaultPriv }}
                    </span>
                </td>
                <td class="py-2 px-3 text-center">
                    <span :class="pub.hope === 'Ungido' ? 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 font-bold' : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300'" class="px-2 py-0.5 rounded text-[7pt] font-semibold">
                      {{ pub.hope || 'Outras Ovelhas' }}
                    </span>
                </td>
                <td class="py-2 px-2.5 text-center text-[7.5pt] text-slate-600 dark:text-slate-400">
                  {{ formatDate(pub.birthDate) }}
                </td>
                <td class="py-2 px-2.5 text-center text-[7.5pt] text-slate-600 dark:text-slate-400">
                  {{ formatDate(pub.baptismDate) }}
                </td>
                <td class="py-2 px-2 text-center">
                    <span :class="pub.active ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-400'" class="px-2 py-0.5 rounded text-[7pt] font-bold">
                      {{ pub.active ? 'Ativo' : 'Inativo' }}
                    </span>
                </td>
                <td class="py-2 px-3 text-slate-600 dark:text-slate-400 text-[8pt]">{{ pub.obs || '—' }}</td>
                <td class="py-2 px-3 text-center no-print">
                  <div class="inline-flex items-center gap-1.5">
                    <button @click="editPublisher(pub)" class="p-1 text-slate-500 hover:text-indigo-600 dark:text-slate-400 dark:hover:text-indigo-300 rounded transition" title="Editar Irmão">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                    </button>
                    <button @click="printPublisherCard(pub.name)" class="inline-flex items-center gap-1 px-2 py-0.5 rounded bg-indigo-50 dark:bg-indigo-950/60 hover:bg-indigo-100 dark:hover:bg-indigo-900 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800 text-[7.5pt] font-semibold shadow-2xs transition" title="Gerar Relatório / Ficha individual em PDF">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                      <span>Relatório PDF</span>
                    </button>
                  </div>
                </td>
              </tr>
              </tbody>
            </table>
          </div>

          <!-- Controles de Paginação: Publicadores -->
          <div v-if="filteredPublishersList.length > 0" class="p-3 border-t border-slate-100 dark:border-slate-800 flex flex-wrap justify-between items-center gap-3 text-xs no-print bg-slate-50/60 dark:bg-slate-900/60">
            <div class="flex items-center gap-2">
              <span class="text-slate-500 dark:text-slate-400 text-[8pt]">Itens por página:</span>
              <select v-model.number="publishersPerPage" class="bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-200 rounded-md px-2 py-1 text-[8pt]">
                <option :value="10">10</option>
                <option :value="20">20</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
                <option :value="9999">Todos</option>
              </select>
              <span class="text-slate-500 dark:text-slate-400 text-[8pt]">
                Mostrando {{ publishersStartIndex + 1 }} - {{ Math.min(publishersStartIndex + publishersPerPage, filteredPublishersList.length) }} de {{ filteredPublishersList.length }}
              </span>
            </div>

            <div class="flex items-center gap-1.5">
              <button
                  @click="publishersCurrentPage = 1"
                  :disabled="publishersCurrentPage <= 1"
                  class="px-2 py-1 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-100 dark:hover:bg-slate-700 font-semibold transition"
                  title="Primeira página"
              >&laquo;</button>
              <button
                  @click="publishersCurrentPage--"
                  :disabled="publishersCurrentPage <= 1"
                  class="px-2.5 py-1 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-100 dark:hover:bg-slate-700 font-semibold transition"
                  title="Página anterior"
              >&lsaquo; Anterior</button>

              <span class="px-2.5 py-1 text-[8pt] font-semibold text-slate-700 dark:text-slate-300">
                Pág. {{ publishersCurrentPage }} de {{ publishersTotalPages }}
              </span>

              <button
                  @click="publishersCurrentPage++"
                  :disabled="publishersCurrentPage >= publishersTotalPages"
                  class="px-2.5 py-1 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-100 dark:hover:bg-slate-700 font-semibold transition"
                  title="Próxima página"
              >Próxima &rsaquo;</button>
              <button
                  @click="publishersCurrentPage = publishersTotalPages"
                  :disabled="publishersCurrentPage >= publishersTotalPages"
                  class="px-2 py-1 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-100 dark:hover:bg-slate-700 font-semibold transition"
                  title="Última página"
              >&raquo;</button>
            </div>
          </div>
        </main>

        <!-- ABA 4: GESTÃO DE GRUPOS -->
        <main v-if="currentTab === 'groups'" class="space-y-4">
          <div class="flex justify-between items-center bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 no-print">
            <div>
              <h2 class="font-bold text-sm text-slate-900 dark:text-white">Organização de Grupos de Serviço</h2>
              <p class="text-[7.5pt] text-slate-500 dark:text-slate-400">Total de {{ groups.length }} grupos cadastrados</p>
            </div>
            <button @click="openGroupModal()" class="inline-flex items-center gap-1.5 bg-emerald-700 hover:bg-emerald-800 text-white px-3.5 py-1.5 rounded-lg text-xs font-semibold shadow-xs transition">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
              <span>Novo Grupo</span>
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
            <div v-for="g in groups" :key="g.name" class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-3.5 shadow-2xs">
              <div class="flex justify-between items-start mb-2 pb-2 border-b border-slate-100 dark:border-slate-800">
                <div>
                  <div class="flex items-center gap-1.5">
                    <h3 class="font-bold text-xs text-slate-900 dark:text-white">{{ g.name }}</h3>
                    <button @click="editGroup(g)" title="Editar Dirigente / Ajudante" class="text-slate-400 hover:text-indigo-600 no-print">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
                    </button>
                  </div>
                  <div class="text-[7pt] text-slate-500 dark:text-slate-400 mt-0.5 space-y-0.5">
                    <div v-if="g.overseer"><strong>Dirigente:</strong> {{ g.overseer }}</div>
                    <div v-if="g.assistant"><strong>Ajudante:</strong> {{ g.assistant }}</div>
                    <div v-if="g.meeting_place"><strong>Saída:</strong> {{ g.meeting_place }}</div>
                  </div>
                </div>
                <span class="text-[7.5pt] bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 px-2 py-0.5 rounded-full font-bold">
                  {{ publishersInGroup(g.name).length }} irmãos
                </span>
              </div>

              <ul class="space-y-1.5 text-[8pt]">
                <li v-for="p in publishersInGroup(g.name)" :key="p.name" class="flex justify-between items-center py-0.5 border-b border-slate-50 dark:border-slate-800/40 last:border-none">
                  <span class="font-medium text-slate-800 dark:text-slate-200 truncate pr-2">{{ p.name }}</span>
                  <div class="flex items-center gap-1 shrink-0 no-print">
                    <span class="text-[6.5pt] text-slate-400">Mover:</span>
                    <select @change="reassignGroup(p, $event)" class="text-[7pt] bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1.5 py-0.5 text-slate-800 dark:text-slate-100">
                      <option v-for="targetG in groupNames" :key="targetG" :value="targetG" :selected="targetG === g.name">
                        {{ targetG }}
                      </option>
                    </select>
                  </div>
                </li>
                <li v-if="publishersInGroup(g.name).length === 0" class="text-center py-3 text-slate-400 italic text-[7.5pt]">
                  Nenhum irmão vinculado a este grupo.
                </li>
              </ul>
            </div>
          </div>
        </main>

        <!-- MODAL DE LANÇAR RELATÓRIO -->
        <div v-if="showReportModal" class="fixed inset-0 z-50 flex items-center justify-center p-3 bg-slate-950/60 backdrop-blur-xs no-print">
          <div class="bg-white dark:bg-slate-900 w-full max-w-lg rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 p-5 space-y-4">
            <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
              <h3 class="font-bold text-base text-slate-900 dark:text-white">
                {{ modalReport.id ? 'Editar Relatório' : 'Lançar Novo Relatório' }}
              </h3>
              <button @click="showReportModal = false" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-lg">&times;</button>
            </div>

            <form @submit.prevent="submitReport" class="space-y-3">
              <div>
                <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Publicador</label>
                <select v-model="modalReport.name" @change="onModalPublisherChange" required class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-800 dark:text-slate-100">
                  <option value="" disabled>Selecione um publicador...</option>
                  <option v-for="p in activePublishers" :key="p.name" :value="p.name">{{ p.name }} ({{ p.group }})</option>
                </select>
              </div>

              <div class="grid grid-cols-3 gap-2">
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Ano Teocrático</label>
                  <select v-model="modalReport.service_year" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                    <option v-for="yr in availableServiceYears" :key="yr" :value="yr">{{ yr }}</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Mês</label>
                  <select v-model="modalReport.month" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                    <option v-for="m in theocraticMonths" :key="m" :value="m">{{ m }}</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Grupo</label>
                  <select v-model="modalReport.group" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                    <option v-for="g in groupNames" :key="g" :value="g">{{ g }}</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Privilégio</label>
                  <select v-model="modalReport.privilege" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                    <option value="Publicador Batizado(a)">Publicador Batizado(a)</option>
                    <option value="Publicador não Batizado(a)">Publicador não Batizado(a)</option>
                    <option value="Pioneiro Regular">Pioneiro Regular</option>
                    <option value="Pioneiro Auxiliar">Pioneiro Auxiliar</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Trabalhou no Campo?</label>
                  <select v-model="modalReport.worked" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100 font-semibold">
                    <option value="Sim">Sim (Trabalhou)</option>
                    <option value="Não">Não (Não trabalhou / Doente)</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-3 gap-3">
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Horas</label>
                  <input v-model.number="modalReport.hours" type="number" min="0" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100" />
                </div>
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Revisitas</label>
                  <input v-model.number="modalReport.revisitas" type="number" min="0" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100" />
                </div>
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Estudos Bíblicos</label>
                  <input v-model.number="modalReport.estudos" type="number" min="0" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100 font-bold text-indigo-600 dark:text-indigo-400" />
                </div>
              </div>

              <div>
                <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Observações</label>
                <input v-model="modalReport.obs" type="text" placeholder="Ex: Doente, Escola de Pioneiros..." class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100" />
              </div>

              <div class="flex justify-end gap-2 pt-3 border-t border-slate-100 dark:border-slate-800">
                <button type="button" @click="showReportModal = false" class="px-3.5 py-1.5 text-xs text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition">Cancelar</button>
                <button type="submit" class="px-4 py-1.5 text-xs bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow-sm transition">Salvar Relatório</button>
              </div>
            </form>
          </div>
        </div>

        <!-- MODAL DE CRIAR / EDITAR GRUPO -->
        <div v-if="showGroupModal" class="fixed inset-0 z-50 flex items-center justify-center p-3 bg-slate-950/60 backdrop-blur-xs no-print">
          <div class="bg-white dark:bg-slate-900 w-full max-w-md rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 p-5 space-y-4">
            <h3 class="font-bold text-base text-slate-900 dark:text-white">
              {{ modalGroup.id ? 'Editar Grupo' : 'Novo Grupo de Serviço' }}
            </h3>
            <form @submit.prevent="submitGroup" class="space-y-3">
              <div>
                <label class="block text-[7.5pt] font-bold mb-1">Nome do Grupo</label>
                <input v-model="modalGroup.name" required placeholder="Ex: Grupo 7" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2" />
              </div>
              <div>
                <label class="block text-[7.5pt] font-bold mb-1">Superintendente (Dirigente)</label>
                <input v-model="modalGroup.overseer" placeholder="Nome do irmão dirigente" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2" />
              </div>
              <div>
                <label class="block text-[7.5pt] font-bold mb-1">Ajudante</label>
                <input v-model="modalGroup.assistant" placeholder="Nome do ajudante" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2" />
              </div>
              <div>
                <label class="block text-[7.5pt] font-bold mb-1">Local da Saída</label>
                <input v-model="modalGroup.meeting_place" placeholder="Ex: Salão do Reino / Casa do irmão" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2" />
              </div>
              <div class="flex justify-end gap-2 pt-3 border-t">
                <button type="button" @click="showGroupModal = false" class="px-3.5 py-1.5 text-xs text-slate-500">Cancelar</button>
                <button type="submit" class="px-4 py-1.5 text-xs bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg font-semibold">Salvar Grupo</button>
              </div>
            </form>
          </div>
        </div>

        <!-- MODAL DE CONFIRMAÇÃO DE EXCLUSÃO DE RELATÓRIO -->
        <div v-if="reportToDelete" class="fixed inset-0 z-50 flex items-center justify-center p-3 bg-slate-950/60 backdrop-blur-xs no-print">
          <div class="bg-white dark:bg-slate-900 w-full max-w-sm rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 p-5 space-y-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-rose-100 dark:bg-rose-950/80 text-rose-600 flex items-center justify-center shrink-0">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <div>
                <h3 class="font-bold text-sm text-slate-900 dark:text-white">Excluir Relatório</h3>
                <p class="text-xs text-slate-500 dark:text-slate-400">Esta ação não poderá ser desfeita.</p>
              </div>
            </div>
            <p class="text-xs text-slate-700 dark:text-slate-300">
              Tem certeza que deseja remover o relatório de <strong>{{ reportToDelete.name }}</strong> referente a <strong>{{ reportToDelete.month }}/{{ reportToDelete.service_year }}</strong>?
            </p>
            <div class="flex justify-end gap-2 pt-2 border-t border-slate-100 dark:border-slate-800">
              <button type="button" @click="reportToDelete = null" class="px-3.5 py-1.5 text-xs text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition">Cancelar</button>
              <button type="button" @click="executeDeleteReport" class="px-4 py-1.5 text-xs bg-rose-600 hover:bg-rose-700 active:bg-rose-800 text-white font-semibold rounded-lg shadow-sm transition">Excluir</button>
            </div>
          </div>
        </div>

        <!-- MODAL DE CADASTRO / EDIÇÃO DE PUBLICADOR -->
        <div v-if="showPublisherModal" class="fixed inset-0 z-50 flex items-center justify-center p-3 bg-slate-950/60 backdrop-blur-xs no-print">
          <div class="bg-white dark:bg-slate-900 w-full max-w-lg rounded-2xl shadow-xl border border-slate-200 dark:border-slate-800 p-5 space-y-4">
            <div class="flex justify-between items-center border-b border-slate-100 dark:border-slate-800 pb-3">
              <h3 class="font-bold text-base text-slate-900 dark:text-white">
                {{ modalPub.id ? 'Editar Dados do Publicador' : 'Cadastrar Novo Publicador' }}
              </h3>
              <button @click="showPublisherModal = false" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-lg">&times;</button>
            </div>

            <form @submit.prevent="submitPublisher" class="space-y-3">
              <div>
                <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Nome Completo</label>
                <input v-model="modalPub.name" type="text" required placeholder="Nome do irmão(ã)" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-3 py-2 text-slate-800 dark:text-slate-100" />
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Gênero</label>
                  <select v-model="modalPub.gender" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                    <option value="Masculino">Masculino</option>
                    <option value="Feminino">Feminino</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Esperança</label>
                  <select v-model="modalPub.hope" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100 font-semibold">
                    <option value="Outras Ovelhas">Outras Ovelhas (Grande Multidão)</option>
                    <option value="Ungido">Ungido</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Grupo de Serviço</label>
                  <select v-model="modalPub.group" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                    <option v-for="g in groupNames" :key="g" :value="g">{{ g }}</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Privilégio Habitual</label>
                  <select v-model="modalPub.defaultPriv" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100">
                    <option value="Publicador Batizado(a)">Publicador Batizado(a)</option>
                    <option value="Publicador não Batizado(a)">Pub. Não Batizado(a)</option>
                    <option value="Pioneiro Regular">Pioneiro Regular</option>
                    <option value="Pioneiro Auxiliar">Pioneiro Auxiliar</option>
                  </select>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Data de Nascimento</label>
                  <input v-model="modalPub.birthDate" type="date" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100" />
                </div>
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Data de Batismo</label>
                  <input v-model="modalPub.baptismDate" type="date" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100" />
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Status</label>
                  <select v-model="modalPub.active" class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100 font-medium">
                    <option :value="true">Ativo</option>
                    <option :value="false">Inativo / Fora da lista</option>
                  </select>
                </div>
                <div>
                  <label class="block text-[7.5pt] font-bold text-slate-700 dark:text-slate-300 mb-1">Observações</label>
                  <input v-model="modalPub.obs" type="text" placeholder="Ex: Novo batizado, transferido..." class="w-full text-xs bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg px-2.5 py-1.5 text-slate-800 dark:text-slate-100" />
                </div>
              </div>

              <div class="flex justify-end gap-2 pt-3 border-t border-slate-100 dark:border-slate-800">
                <button type="button" @click="showPublisherModal = false" class="px-3.5 py-1.5 text-xs text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition">Cancelar</button>
                <button type="submit" class="px-4 py-1.5 text-xs bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow-sm transition">Salvar Cadastro</button>
              </div>
            </form>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';
import { api, type Publisher, type Report, type Group } from './services/api';

// --- Constantes Teocráticas ---
const theocraticMonths = [
  "Outubro", "Novembro", "Dezembro", "Janeiro", "Fevereiro", "Março",
  "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro"
];

const calendarMonths = [
  "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
  "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

const availableServiceYears = ref(['2025/2026', '2026/2027', '2027/2028']);

// --- Estado Reativo ---
const isDark = ref(localStorage.getItem('theme_mode') === 'dark');
const currentTab = ref('reports');
const dbConnected = ref(false);

const selectedServiceYear = ref('2026/2027');
const selectedMonth = ref('Outubro');
const selectedGroup = ref('all');
const selectedPrivilege = ref('all');
const searchQuery = ref('');

// --- Paginação Reativa: Relatórios e Publicadores ---
const reportsCurrentPage = ref(1);
const reportsPerPage = ref(15);

const publishersCurrentPage = ref(1);
const publishersPerPage = ref(15);

// Reseta páginas ao mudar filtros ou busca
watch([selectedServiceYear, selectedMonth, selectedGroup, selectedPrivilege, searchQuery], () => {
  reportsCurrentPage.value = 1;
  publishersCurrentPage.value = 1;
});

// --- Função de correspondência do Filtro de Privilégio ---
function matchesPrivilegeFilter(privilegeText?: string) {
  if (!selectedPrivilege.value || selectedPrivilege.value === 'all') return true;
  if (!privilegeText) return false;
  const p = privilegeText.toLowerCase();

  switch (selectedPrivilege.value) {
    case 'PR':
      return p.includes('regular');
    case 'PA':
      return p.includes('auxiliar');
    case 'PNB':
      return p.includes('não batizado') || p.includes('nao batizado');
    case 'PB':
      // Publicador Batizado: deve ter "batizado", mas NÃO "não batizado", "regular" ou "auxiliar"
      return (p.includes('batizado') || p.includes('publicador')) &&
          !p.includes('não') &&
          !p.includes('nao') &&
          !p.includes('regular') &&
          !p.includes('auxiliar');
    default:
      return p.includes(selectedPrivilege.value.toLowerCase());
  }
}

// --- Grupos Reativos ---
const groups = ref<Group[]>([
  { id: 1, name: "Grupo 1", overseer: "", assistant: "", meeting_place: "", active: true },
  { id: 2, name: "Grupo 2", overseer: "", assistant: "", meeting_place: "", active: true },
  { id: 3, name: "Grupo 3", overseer: "", assistant: "", meeting_place: "", active: true },
  { id: 4, name: "Grupo 4", overseer: "", assistant: "", meeting_place: "", active: true },
  { id: 5, name: "Grupo 5", overseer: "", assistant: "", meeting_place: "", active: true },
  { id: 6, name: "Grupo 6", overseer: "", assistant: "", meeting_place: "", active: true }
]);

const groupNames = computed(() => groups.value.map(g => g.name));

// --- Roster Completo dos Irmãos Cadastrados (com Heitor incluso) ---
const publishers = ref<Publisher[]>([
  // GRUPO 1 (15)
  { id: "pub_1_1", name: "Ana Carolina", group: "Grupo 1", defaultPriv: "Pioneiro Auxiliar", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA frequente" },
  { id: "pub_1_2", name: "Ana Luiza", group: "Grupo 1", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR (horas ajustadas por recuperação/doença)" },
  { id: "pub_1_3", name: "Andrea Cristina da Silva Souza", group: "Grupo 1", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_1_4", name: "Emily da Silva Sousa", group: "Grupo 1", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_1_5", name: "Felipe", group: "Grupo 1", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_1_6", name: "Irene Amaral", group: "Grupo 1", defaultPriv: "Pioneiro Auxiliar", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA frequente" },
  { id: "pub_1_7", name: "Izequiel Garcia", group: "Grupo 1", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_1_8", name: "José Gomes Filho", group: "Grupo 1", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_1_9", name: "Maria De Jesus Souza", group: "Grupo 1", defaultPriv: "Pioneiro Auxiliar", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Iniciou acompanhamento em Julho" },
  { id: "pub_1_10", name: "Maria de Lourdes Amaral", group: "Grupo 1", defaultPriv: "Pioneiro Auxiliar", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA frequente" },
  { id: "pub_1_11", name: "Marisa Camargo Garcia", group: "Grupo 1", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_1_12", name: "Nelson Manso", group: "Grupo 1", defaultPriv: "Pioneiro Regular", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR constante (~50h)" },
  { id: "pub_1_13", name: "Raquel de Souza Lima Holanda", group: "Grupo 1", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_1_14", name: "Rodrigo Cardoso Medeiros", group: "Grupo 1", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_1_15", name: "Valmir de Souza Holanda", group: "Grupo 1", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },

  // GRUPO 2 (22)
  { id: "pub_2_1", name: "Antônio Rodrigues de Souza", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_2", name: "Bruna Cristina da Silva", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_3", name: "Clarisa Maria Gregorio Rodrigues de Souza", group: "Grupo 2", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR (40h a 50h)" },
  { id: "pub_2_4", name: "Cleosdeti da Silva", group: "Grupo 2", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR com revisitas constantes" },
  { id: "pub_2_5", name: "Daniel Emidio dos Santos", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_6", name: "Daniel Landim", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_7", name: "Geraldo Soares Landim", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_8", name: "Glaucio Landim", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_9", name: "Guilherme Pereira Ribeiro", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_10", name: "Joel Marques da Silva", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_11", name: "Josiane Cristina Ferreira da Silva", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_12", name: "Josiane Pereira Ribeiro", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_13", name: "Júlia Rafaela da Silva", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_14", name: "Lidia Silveira da Silva", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_15", name: "Madalena Gonçalves da Silva", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_16", name: "Marcia Aparecida de Oliveira Silva", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_17", name: "Maria Zilda", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_18", name: "Monica Landim", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_19", name: "Pamela Maria dos Santos", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_20", name: "Raimundo de Oliveira Filho", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_21", name: "Sergio Anderson Manço da Silva", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_2_22", name: "Wagton Reis Ribeiro", group: "Grupo 2", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },

  // GRUPO 3 (18)
  { id: "pub_3_1", name: "Adriana Cristina da Silva Mizuno", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_2", name: "Adriana de Paula Sá de Freitas", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_3", name: "Ana Cláudia Martins", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_4", name: "André Fabiano Ferreira de Freitas", group: "Grupo 3", defaultPriv: "Pioneiro Regular", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR (Escola de Pioneiros)" },
  { id: "pub_3_5", name: "Cecília Teixeira", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_6", name: "Creusimar Alves de Silva", group: "Grupo 3", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR constante" },
  { id: "pub_3_7", name: "Helena Pereira de Souza dos Santos", group: "Grupo 3", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR constante" },
  { id: "pub_3_8", name: "Irma Lopes de Paula", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_9", name: "João Victor", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Iniciou em Agosto (PA 15h)" },
  { id: "pub_3_10", name: "Kananda Freitas", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_11", name: "Laura Faleiros", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_12", name: "Nelson Donizete da Silva", group: "Grupo 3", defaultPriv: "Pioneiro Regular", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR (Escola de Pioneiros)" },
  { id: "pub_3_13", name: "Rilma Nascimento de Assis", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_14", name: "Roberta Primeiro", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_15", name: "Rosângela", group: "Grupo 3", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR constante" },
  { id: "pub_3_16", name: "Suzane Raffaelle Pereira dos Santos", group: "Grupo 3", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_3_17", name: "Tayla Sofhia Nascimento", group: "Grupo 3", defaultPriv: "Publicador não Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Pub. Não Batizado(a)" },
  { id: "pub_3_18", name: "Vilma", group: "Grupo 3", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR (50h a 70h)" },
  { id: "pub_3_19", name: "Vinícius Nascimento", group: "Grupo 3", defaultPriv: "Publicador não Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Pub. Não Batizado(a)" },

  // GRUPO 4 (15)
  { id: "pub_4_1", name: "Adriano Junior dos Santos", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_2", name: "Aparecido Oliveira", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_3", name: "Carmem Lucia Machado da Silva Oliveira", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_4", name: "Claudineia Gomes Teixeira de Freitas", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_5", name: "Elaine Alves Ferreira", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_6", name: "Eva Andrade", group: "Grupo 4", defaultPriv: "Pioneiro Auxiliar", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA frequente" },
  { id: "pub_4_7", name: "Fernando", group: "Grupo 4", defaultPriv: "Pioneiro Auxiliar", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA frequente" },
  { id: "pub_4_8", name: "Gabriel Barbosa dos Santos Leal", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_9", name: "Gabriel Machado", group: "Grupo 4", defaultPriv: "Publicador não Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Pub. Não Batizado(a)" },
  { id: "pub_4_10", name: "Kaique", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_11", name: "Lara", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_12", name: "Maisa", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_13", name: "Maria José Ramos", group: "Grupo 4", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR (53h a 70h)" },
  { id: "pub_4_14", name: "Nadia", group: "Grupo 4", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_4_15", name: "Nubia", group: "Grupo 4", defaultPriv: "Pioneiro Auxiliar", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA contínua" },

  // GRUPO 5 (22)
  { id: "pub_5_1", name: "Adriano Macedo", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_2", name: "Ana Lucia Santos", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_3", name: "Aurea", group: "Grupo 5", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR Especial idosa" },
  { id: "pub_5_4", name: "Dalva Nicolau", group: "Grupo 5", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR constante (50h)" },
  { id: "pub_5_5", name: "Devair Rodrigues", group: "Grupo 5", defaultPriv: "Pioneiro Auxiliar", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA constante" },
  { id: "pub_5_6", name: "Divina", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_7", name: "José Antonio", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_8", name: "José Barbosa", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_9", name: "Kamila Sousa", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_10", name: "Lidia Faleiros", group: "Grupo 5", defaultPriv: "Pioneiro Auxiliar", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA frequente" },
  { id: "pub_5_11", name: "Lindalva Ribeiro", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_12", name: "Luiza Maria Silva Barbosa", group: "Grupo 5", defaultPriv: "Publicador não Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Pub. Não Batizado(a)" },
  { id: "pub_5_13", name: "Marcia Macedo", group: "Grupo 5", defaultPriv: "Pioneiro Auxiliar", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA contínua (30h)" },
  { id: "pub_5_14", name: "Marcio Antonio de Souza", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_15", name: "Maria Aparecida Souza", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_16", name: "Maria de Jesus Santos", group: "Grupo 5", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR dedicada (~50h)" },
  { id: "pub_5_17", name: "Maria Lucia Rodrigues", group: "Grupo 5", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR fiel (50h)" },
  { id: "pub_5_18", name: "Marli Nascimento", group: "Grupo 5", defaultPriv: "Pioneiro Regular", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PR constante (50h)" },
  { id: "pub_5_19", name: "Polliane", group: "Grupo 5", defaultPriv: "Publicador não Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Pub. Não Batizado(a)" },
  { id: "pub_5_20", name: "Raimundo Neto", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_5_21", name: "Walison", group: "Grupo 5", defaultPriv: "Publicador não Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Pub. Não Batizado(a)" },
  { id: "pub_5_22", name: "Willian", group: "Grupo 5", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },

  // GRUPO 6 (12 - com HEITOR)
  { id: "pub_6_1", name: "Daniela", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_6_2", name: "Elen", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Mantém 2 estudos bíblicos todo mês" },
  { id: "pub_6_3", name: "Florisvaldo Ferreira Filho", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_6_heitor", name: "Heitor", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Novo integrante do Grupo 6" },
  { id: "pub_6_4", name: "Juscileide", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_6_5", name: "Maion", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_6_6", name: "Marise", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_6_7", name: "Osmair", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_6_8", name: "Tania", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_6_9", name: "Valdecir", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "" },
  { id: "pub_6_10", name: "Valdina de Jesus Santos Ferreira", group: "Grupo 6", defaultPriv: "Pioneiro Auxiliar", gender: "Feminino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "PA frequente" },
  { id: "pub_6_11", name: "Walter Bonfim Santana", group: "Grupo 6", defaultPriv: "Publicador Batizado(a)", gender: "Masculino", birthDate: "", baptismDate: "", hope: "Outras Ovelhas", active: true, obs: "Transferido do G2 para o G6" }
]);

// --- Base de Relatórios Sincronizados de Outubro ---
const reports = ref<Report[]>([
  { id: 1, name: "Adriana Cristina da Silva Mizuno", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 2, name: "Adriana de Paula Sá de Freitas", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 1, worked: "Sim", obs: "" },
  { id: 3, name: "Adriano Junior dos Santos", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 1, worked: "Sim", obs: "" },
  { id: 4, name: "Ana Cláudia Martins", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 5, name: "André Fabiano Ferreira de Freitas", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Regular", hours: 48, revisitas: 0, estudos: 2, worked: "Sim", obs: "" },
  { id: 6, name: "Aparecido Oliveira", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 7, name: "Bruna Cristina da Silva", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 8, name: "Carmem Lucia Machado da Silva Oliveira", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 9, name: "Cecília Teixeira", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 10, name: "Clarisa Maria Gregorio Rodrigues de Souza", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Regular", hours: 46, revisitas: 0, estudos: 0, worked: "Sim", obs: "Ficou doente por isso não completou o requisito" },
  { id: 11, name: "Claudineia Gomes Teixeira de Freitas", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 12, name: "Cleosdeti da Silva", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Regular", hours: 50, revisitas: 10, estudos: 0, worked: "Sim", obs: "" },
  { id: 13, name: "Creusimar Alves de Silva", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Regular", hours: 53, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 14, name: "Daniel Emidio dos Santos", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 15, name: "Daniel Landim", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 16, name: "Elaine Alves Ferreira", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 17, name: "Eva Andrade", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Auxiliar", hours: 0, revisitas: 0, estudos: 2, worked: "Sim", obs: "" },
  { id: 18, name: "Fernando", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Auxiliar", hours: 0, revisitas: 0, estudos: 1, worked: "Sim", obs: "" },
  { id: 19, name: "Gabriel Barbosa dos Santos Leal", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 2, worked: "Sim", obs: "" },
  { id: 20, name: "Gabriel Machado", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador não Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 21, name: "Geraldo Soares Landim", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 22, name: "Glaucio Landim", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 23, name: "Guilherme Pereira Ribeiro", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 24, name: "Helena Pereira de Souza dos Santos", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Regular", hours: 31, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 25, name: "Irma Lopes de Paula", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 26, name: "João Victor", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 27, name: "Josiane Cristina Ferreira da Silva", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 28, name: "Josiane Pereira Ribeiro", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 29, name: "Júlia Rafaela da Silva", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 30, name: "Kaique", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 31, name: "Kananda Freitas", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 32, name: "Lara", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 33, name: "Laura Faleiros", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 1, worked: "Sim", obs: "" },
  { id: 34, name: "Lidia Silveira da Silva", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 35, name: "Maisa", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 36, name: "Marcia Aparecida de Oliveira Silva", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 37, name: "Maria José Ramos", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Regular", hours: 60, revisitas: 0, estudos: 1, worked: "Sim", obs: "" },
  { id: 38, name: "Maria Zilda", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 39, name: "Monica Landim", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 40, name: "Nadia", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 2, worked: "Sim", obs: "" },
  { id: 41, name: "Nelson Donizete da Silva", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Regular", hours: 52, revisitas: 0, estudos: 6, worked: "Sim", obs: "" },
  { id: 42, name: "Nubia", group: "Grupo 4", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Auxiliar", hours: 0, revisitas: 0, estudos: 1, worked: "Sim", obs: "" },
  { id: 43, name: "Pamela Maria dos Santos", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 44, name: "Raimundo de Oliveira Filho", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 45, name: "Rilma Nascimento de Assis", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 1, worked: "Sim", obs: "" },
  { id: 46, name: "Roberta Primeiro", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 47, name: "Rosângela", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Regular", hours: 40, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 48, name: "Sergio Anderson Manço da Silva", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 1, worked: "Sim", obs: "" },
  { id: 49, name: "Suzane Raffaelle Pereira dos Santos", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 50, name: "Tayla Sofhia Nascimento", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador não Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 51, name: "Vilma", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Pioneiro Regular", hours: 50, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 52, name: "Vinícius Nascimento", group: "Grupo 3", month: "Outubro", service_year: "2026/2027", privilege: "Publicador não Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" },
  { id: 53, name: "Wagton Reis Ribeiro", group: "Grupo 2", month: "Outubro", service_year: "2026/2027", privilege: "Publicador Batizado(a)", hours: 0, revisitas: 0, estudos: 0, worked: "Sim", obs: "" }
]);

// --- Modais Reativos ---
const showReportModal = ref(false);
const showPublisherModal = ref(false);
const showGroupModal = ref(false);
const reportToDelete = ref<Report | null>(null);
const copySuccessToast = ref(false);
const saveSuccessMessage = ref('');

function showNotification(msg: string) {
  saveSuccessMessage.value = msg;
  setTimeout(() => {
    saveSuccessMessage.value = '';
  }, 3500);
}

const modalReport = ref<Report>({
  id: undefined,
  name: '',
  group: 'Grupo 1',
  month: 'Outubro',
  service_year: '2026/2027',
  privilege: 'Publicador Batizado(a)',
  hours: 0,
  revisitas: 0,
  estudos: 0,
  worked: 'Sim',
  obs: ''
});

const modalPub = ref<Publisher>({
  id: '',
  name: '',
  group: 'Grupo 1',
  defaultPriv: 'Publicador Batizado(a)',
  gender: 'Masculino',
  birthDate: '',
  baptismDate: '',
  hope: 'Outras Ovelhas',
  active: true,
  obs: ''
});

const modalGroup = ref<Group>({
  id: undefined,
  name: '',
  overseer: '',
  assistant: '',
  meeting_place: '',
  active: true
});

// --- Computados ---
const activePublishers = computed(() => publishers.value.filter(p => p.active));

const regularPioneersList = computed(() => {
  return activePublishers.value
      .filter(p => p.defaultPriv && p.defaultPriv.toLowerCase().includes('regular'))
      .sort((a, b) => a.name.localeCompare(b.name, 'pt-BR'));
});

function getPioneerNumber(publisherName: string) {
  const idx = regularPioneersList.value.findIndex(p => p.name === publisherName);
  return idx !== -1 ? (idx + 1) : null;
}

const deliveredReports = computed(() => {
  return reports.value.filter(r => {
    const matchYear = !selectedServiceYear.value || selectedServiceYear.value === 'all' || r.service_year === selectedServiceYear.value;
    const matchMonth = !selectedMonth.value || selectedMonth.value === 'all' || r.month === selectedMonth.value;
    return matchYear && matchMonth;
  });
});

const filteredReports = computed(() => {
  return deliveredReports.value.filter(r => {
    const matchGroup = selectedGroup.value === 'all' || r.group === selectedGroup.value;
    const matchPriv = matchesPrivilegeFilter(r.privilege);
    const matchSearch = !searchQuery.value || r.name.toLowerCase().includes(searchQuery.value.toLowerCase().trim());
    return matchGroup && matchPriv && matchSearch;
  });
});

// --- Computados da Paginação de Relatórios ---
const reportsTotalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredReports.value.length / reportsPerPage.value));
});

const reportsStartIndex = computed(() => {
  return (reportsCurrentPage.value - 1) * reportsPerPage.value;
});

const paginatedReports = computed(() => {
  return filteredReports.value.slice(
      reportsStartIndex.value,
      reportsStartIndex.value + reportsPerPage.value
  );
});

const pendingPublishers = computed(() => {
  const currentMonthName = selectedMonth.value === 'all' ? 'Outubro' : selectedMonth.value;
  const currentYearName = selectedServiceYear.value === 'all' ? '2026/2027' : selectedServiceYear.value;

  const deliveredNames = new Set(
      reports.value
          .filter(r => r.month === currentMonthName && (r.service_year === currentYearName || !r.service_year))
          .map(r => r.name)
  );

  return activePublishers.value.filter(p => {
    const isPending = !deliveredNames.has(p.name);
    const matchGroup = selectedGroup.value === 'all' || p.group === selectedGroup.value;
    const matchPriv = matchesPrivilegeFilter(p.defaultPriv);
    const matchSearch = !searchQuery.value || p.name.toLowerCase().includes(searchQuery.value.toLowerCase().trim());
    return isPending && matchGroup && matchPriv && matchSearch;
  });
});

const filteredPublishersList = computed(() => {
  return activePublishers.value.filter(p => {
    const matchGroup = selectedGroup.value === 'all' || p.group === selectedGroup.value;
    const matchPriv = matchesPrivilegeFilter(p.defaultPriv);
    const matchSearch = !searchQuery.value || p.name.toLowerCase().includes(searchQuery.value.toLowerCase().trim());
    return matchGroup && matchPriv && matchSearch;
  });
});

// --- Computados da Paginação de Publicadores ---
const publishersTotalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredPublishersList.value.length / publishersPerPage.value));
});

const publishersStartIndex = computed(() => {
  return (publishersCurrentPage.value - 1) * publishersPerPage.value;
});

const paginatedPublishers = computed(() => {
  return filteredPublishersList.value.slice(
      publishersStartIndex.value,
      publishersStartIndex.value + publishersPerPage.value
  );
});

const stats = computed(() => {
  let totalHours = 0, studies = 0, worked = 0, pr = 0, pa = 0, pb = 0, pnb = 0;

  filteredReports.value.forEach(r => {
    totalHours += Number(r.hours) || 0;
    studies += Number(r.estudos) || 0;
    if (r.worked !== 'Não') worked++;

    if (r.privilege.includes('Regular')) pr++;
    else if (r.privilege.includes('Auxiliar')) pa++;
    else if (r.privilege.includes('não Batizado')) pnb++;
    else pb++;
  });

  const count = filteredReports.value.length;
  const avgHours = count > 0 ? (totalHours / count).toFixed(1) : '0.0';

  return { totalHours, studies, worked, pr, pa, pb, pnb, avgHours };
});

// --- Métodos de Apoio e Banco ---
function groupPending(groupName: string) {
  return pendingPublishers.value.filter(p => p.group === groupName);
}

function publishersInGroup(groupName: string) {
  return activePublishers.value.filter(p => p.group === groupName);
}

function getPrivilegeBadgeClass(priv: string) {
  if (priv?.includes('Regular')) return 'bg-purple-100 text-purple-800 dark:bg-purple-950 dark:text-purple-300';
  if (priv?.includes('Auxiliar')) return 'bg-amber-100 text-amber-900 dark:bg-amber-950 dark:text-amber-300';
  if (priv?.includes('não Batizado')) return 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300';
  return 'bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300';
}

function repHoursClass(h: number) {
  if (h >= 50) return 'text-purple-700 dark:text-purple-400';
  if (h > 0) return 'text-slate-900 dark:text-white';
  return 'text-slate-400 dark:text-slate-500 font-normal';
}

function applyTheme(dark: boolean) {
  if (dark) {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme_mode', 'dark');
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('theme_mode', 'light');
  }
}

function toggleDarkMode() {
  isDark.value = !isDark.value;
  applyTheme(isDark.value);
}

function resetToCurrentMonth() {
  const now = new Date();
  const currentMonthIdx = now.getMonth();
  const targetIdx = (currentMonthIdx - 1 + 12) % 12;
  selectedMonth.value = calendarMonths[targetIdx] ?? 'Outubro';
}

function confirmDeleteReport(rep: Report) {
  reportToDelete.value = rep;
}

async function executeDeleteReport() {
  if (!reportToDelete.value) return;
  const target = reportToDelete.value;

  if (dbConnected.value && target.id) {
    try {
      await api.deleteReport(target.id);
    } catch (err) {
      console.error("Erro ao deletar relatório no PostgreSQL:", err);
    }
  }

  const idx = reports.value.findIndex(r =>
      (r.id && target.id && r.id === target.id) ||
      (r.name === target.name && r.month === target.month && r.service_year === target.service_year)
  );
  if (idx !== -1) {
    reports.value.splice(idx, 1);
  }

  saveData();
  reportToDelete.value = null;
}

async function reassignGroup(pub: Publisher, ev: Event) {
  const newGroup = (ev.target as HTMLSelectElement).value;
  pub.group = newGroup;

  const matchedGroup = groups.value.find(g => g.name === newGroup);
  if (matchedGroup && matchedGroup.id) {
    pub.group_id = matchedGroup.id;
  }

  if (dbConnected.value) {
    try {
      await api.savePublisher(pub);
    } catch (err) {
      console.error("Erro ao salvar publicador no banco:", err);
    }
  }
  saveData();
}

function openGroupModal() {
  modalGroup.value = {
    id: undefined,
    name: `Grupo ${groups.value.length + 1}`,
    overseer: '',
    assistant: '',
    meeting_place: '',
    active: true
  };
  showGroupModal.value = true;
}

function editGroup(g: Group) {
  modalGroup.value = { ...g };
  showGroupModal.value = true;
}

async function submitGroup() {
  const g = { ...modalGroup.value };

  if (dbConnected.value) {
    try {
      const res = await api.saveGroup(g);
      if (res && res.id) g.id = res.id;
    } catch (e) {
      console.error("Erro ao salvar grupo na API:", e);
    }
  }

  const idx = groups.value.findIndex(item => item.name === g.name || (item.id && item.id === g.id));
  if (idx !== -1) groups.value[idx] = g;
  else groups.value.push(g);

  saveData();
  showGroupModal.value = false;
}

function openReportModal(initialPub: Publisher | null = null) {
  if (initialPub) {
    modalReport.value = {
      id: undefined,
      name: initialPub.name,
      group: initialPub.group,
      month: selectedMonth.value === 'all' ? 'Outubro' : selectedMonth.value,
      service_year: selectedServiceYear.value,
      privilege: initialPub.defaultPriv,
      hours: 0,
      revisitas: 0,
      estudos: 0,
      worked: 'Sim',
      obs: ''
    };
  } else {
    modalReport.value = {
      id: undefined,
      name: activePublishers.value[0]?.name || '',
      group: activePublishers.value[0]?.group || 'Grupo 1',
      month: selectedMonth.value === 'all' ? 'Outubro' : selectedMonth.value,
      service_year: selectedServiceYear.value,
      privilege: 'Publicador Batizado(a)',
      hours: 0,
      revisitas: 0,
      estudos: 0,
      worked: 'Sim',
      obs: ''
    };
  }
  showReportModal.value = true;
}

function onModalPublisherChange() {
  const found = publishers.value.find(p => p.name === modalReport.value.name);
  if (found) {
    modalReport.value.group = found.group;
    modalReport.value.privilege = found.defaultPriv || 'Publicador Batizado(a)';
  }
}

function editReport(rep: Report) {
  modalReport.value = { ...rep };
  showReportModal.value = true;
}

function quickReport(pub: Publisher) {
  openReportModal(pub);
}

async function submitReport() {
  const reportData = { ...modalReport.value };

  const matchedGroup = groups.value.find(g => g.name === reportData.group);
  if (matchedGroup && matchedGroup.id) {
    reportData.group_id = matchedGroup.id;
  }

  if (dbConnected.value) {
    try {
      const res = await api.saveReport(reportData);
      if (res && res.id) {
        reportData.id = res.id;
        showNotification(`Relatório de ${reportData.name} salvo no PostgreSQL!`);
      }
    } catch (e) {
      console.error("Erro ao salvar relatório no banco:", e);
      showNotification(`Salvo localmente (offline)`);
    }
  } else {
    if (!reportData.id) reportData.id = Date.now();
    showNotification(`Salvo localmente (offline)`);
  }

  const idx = reports.value.findIndex(r =>
      (r.id && reportData.id && r.id === reportData.id) ||
      (r.name === reportData.name && r.month === reportData.month && r.service_year === reportData.service_year)
  );
  if (idx !== -1) {
    reports.value[idx] = reportData;
  } else {
    reports.value.push(reportData);
  }

  saveData();
  showReportModal.value = false;
}

function formatDate(val?: string) {
  if (!val) return '—';
  const parts = val.split('-');
  return parts.length === 3 ? `${parts[2]}/${parts[1]}/${parts[0]}` : val;
}

function openPublisherModal() {
  modalPub.value = {
    id: '',
    name: '',
    group: groupNames.value[0] || 'Grupo 1',
    defaultPriv: 'Publicador Batizado(a)',
    gender: 'Masculino',
    birthDate: '',
    baptismDate: '',
    hope: 'Outras Ovelhas',
    active: true,
    obs: ''
  };
  showPublisherModal.value = true;
}

function editPublisher(pub: Publisher) {
  modalPub.value = { ...pub };
  showPublisherModal.value = true;
}

async function submitPublisher() {
  const pubData = { ...modalPub.value };
  if (!pubData.id) {
    pubData.id = 'pub_' + Date.now();
  }

  const matchedGroup = groups.value.find(g => g.name === pubData.group);
  if (matchedGroup && matchedGroup.id) {
    pubData.group_id = matchedGroup.id;
  }

  if (dbConnected.value) {
    try {
      await api.savePublisher(pubData);
      showNotification(`${pubData.name} gravado no PostgreSQL!`);
    } catch (e) {
      console.error("Erro ao salvar publicador no banco:", e);
      showNotification(`Salvo localmente (offline)`);
    }
  } else {
    showNotification(`Salvo localmente (offline)`);
  }

  const idx = publishers.value.findIndex(p => (p.id && p.id === pubData.id) || p.name === pubData.name);
  if (idx !== -1) {
    publishers.value[idx] = pubData;
  } else {
    publishers.value.push(pubData);
  }

  saveData();
  showPublisherModal.value = false;
}

function saveData() {
  localStorage.setItem('gestao_relatorios_data', JSON.stringify(reports.value));
  localStorage.setItem('gestao_publicadores_data', JSON.stringify(publishers.value));
  localStorage.setItem('gestao_grupos_data', JSON.stringify(groups.value));
}

function exportBackup() {
  const dataToExport = {
    version: "1.0",
    exportDate: new Date().toISOString(),
    publishers: publishers.value,
    reports: reports.value,
    groups: groups.value
  };
  const blob = new Blob([JSON.stringify(dataToExport, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `backup_relatorios_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function importBackup(event: Event) {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const parsed = JSON.parse(e.target?.result as string);
      if (parsed.reports && Array.isArray(parsed.reports)) reports.value = parsed.reports;
      if (parsed.publishers && Array.isArray(parsed.publishers)) publishers.value = parsed.publishers;
      if (parsed.groups && Array.isArray(parsed.groups)) groups.value = parsed.groups;
      saveData();
      alert("Backup restaurado com sucesso!");
    } catch {
      alert("Erro ao ler o arquivo de backup.");
    }
  };
  reader.readAsText(file);
  target.value = '';
}

function generateSinglePublisherCardHTML(pub: Publisher, isBatch = false) {
  const currentSY = selectedServiceYear.value === 'all' ? '2026/2027' : selectedServiceYear.value;
  const pubReports = reports.value.filter(r => r.name === pub.name);

  let totalHours = 0;
  let totalStudies = 0;
  let monthsWorkedCount = 0;

  const rowsHtml = theocraticMonths.map((m, idx) => {
    const rep = pubReports.find(r => r.month === m && (r.service_year === currentSY || !r.service_year));
    const worked = rep ? rep.worked : '—';
    const hours = rep ? Number(rep.hours || 0) : 0;
    const studies = rep ? Number(rep.estudos || 0) : 0;
    const priv = rep ? rep.privilege : (pub.defaultPriv || 'PB');
    const obs = rep ? (rep.obs || '') : '';

    if (rep && rep.worked === 'Sim') {
      monthsWorkedCount++;
      totalHours += hours;
      totalStudies += studies;
    }

    const workedBadge = worked === 'Sim'
        ? '<span style="color: #15803d; font-weight: bold; background: #dcfce7; padding: 2px 7px; border-radius: 4px; font-size: 7.5pt;">Sim (Trabalhou)</span>'
        : worked === 'Não'
            ? '<span style="color: #b91c1c; font-weight: bold; background: #fee2e2; padding: 2px 7px; border-radius: 4px; font-size: 7.5pt;">Não trabalhou</span>'
            : '<span style="color: #94a3b8; font-size: 7.5pt;">Não informado</span>';

    return `
      <tr style="border-bottom: 1px solid #e2e8f0; font-size: 8.5pt;">
        <td style="padding: 5px 6px; text-align: center; color: #64748b;">${idx + 1}</td>
        <td style="padding: 5px 8px; font-weight: 600; color: #1e293b;">${m}</td>
        <td style="padding: 5px 8px; text-align: center;">${workedBadge}</td>
        <td style="padding: 5px 8px; color: #334155;">${rep ? priv : '—'}</td>
        <td style="padding: 5px 8px; text-align: center; font-weight: 700; color: ${hours > 0 ? '#1e1b4b' : '#94a3b8'};">${rep ? hours + ' h' : '—'}</td>
        <td style="padding: 5px 8px; text-align: center; font-weight: 700; color: ${studies > 0 ? '#4338ca' : '#94a3b8'};">${rep ? studies : '—'}</td>
        <td style="padding: 5px 8px; font-size: 8pt; color: #475569; font-style: italic;">${obs || '—'}</td>
      </tr>
    `;
  }).join('');

  const avgHours = monthsWorkedCount > 0 ? (totalHours / monthsWorkedCount).toFixed(1) : '0.0';

  const isPR = (pub.defaultPriv && pub.defaultPriv.toLowerCase().includes('regular')) ||
      pubReports.some(r => r.privilege && r.privilege.toLowerCase().includes('regular'));
  const prNumber = getPioneerNumber(pub.name);
  const ANNUAL_REQUIREMENT = 600;
  const diffHours = totalHours - ANNUAL_REQUIREMENT;
  const progressPerc = Math.min(100, Math.max(0, ((totalHours / ANNUAL_REQUIREMENT) * 100))).toFixed(1);

  let pioneerSectionHtml = '';
  if (isPR) {
    pioneerSectionHtml = `
      <div style="background: linear-gradient(to right, #faf5ff, #f3e8ff); border: 1.5px solid #c084fc; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(147, 51, 234, 0.08);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="background: #7e22ce; color: #ffffff; font-weight: 800; font-size: 8pt; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;">
              PIONEIRO REGULAR ${prNumber ? '#' + prNumber : ''}
            </span>
            <span style="font-size: 8pt; font-weight: 700; color: #581c87;">Requisito Anual: 600 Horas</span>
          </div>
          <div style="font-size: 8.5pt; color: #6b21a8; font-weight: 700;">
            Realizado: <span style="font-size: 11pt; color: #7e22ce; font-weight: 800;">${totalHours} h</span> / 600 h (${progressPerc}%)
          </div>
        </div>
        <div style="background: #e9d5ff; height: 10px; border-radius: 5px; overflow: hidden; margin-bottom: 6px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);">
          <div style="background: linear-gradient(90deg, #9333ea, #7e22ce); height: 100%; width: ${progressPerc}%; border-radius: 5px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 7.5pt; color: #6b21a8;">
          <span>Meta teocrática mensal: <strong>50h / mês</strong></span>
          <span>${diffHours >= 0 ? '<strong style="color: #15803d; font-size: 8pt;">+ ' + diffHours + ' h (Requisito Anual Atingido!)</strong>' : 'Faltam <strong>' + Math.abs(diffHours) + ' h</strong> para completar o requisito anual'}</span>
        </div>
      </div>
    `;
  }

  return `
    <div style="page-break-after: ${isBatch ? 'always' : 'auto'}; margin-bottom: 28px; padding: 16px 18px; border: 1.5px solid #cbd5e1; border-radius: 10px; background: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
      <!-- Topo Institucional -->
      <div style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2.5px solid #4f46e5; padding-bottom: 8px; margin-bottom: 12px;">
        <div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 7pt; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; color: #4338ca;">REGISTRO DE PUBLICADOR DA CONGREGAÇÃO</span>
            ${isPR ? `<span style="background: #7e22ce; color: #ffffff; font-size: 6.5pt; font-weight: 800; padding: 2px 6px; border-radius: 3px;">PR #${prNumber || ''}</span>` : ''}
          </div>
          <h2 style="margin: 4px 0 0 0; font-size: 15pt; color: #0f172a; font-weight: 800; letter-spacing: -0.3px;">${pub.name}</h2>
        </div>
        <div style="text-align: right; font-size: 8.5pt; color: #64748b;">
          <div>Ano de Serviço: <strong style="color: #0f172a;">${currentSY}</strong></div>
          <div>Grupo de Serviço: <strong style="color: #4338ca;">${pub.group}</strong></div>
        </div>
      </div>

      <!-- Grade de Dados Cadastrais -->
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px; margin-bottom: 12px; font-size: 8pt;">
        <div><span style="color: #64748b; font-size: 6.5pt; font-weight: 700; display: block; text-transform: uppercase;">Privilégio</span><strong style="color: #0f172a;">${pub.defaultPriv || 'Publicador Batizado(a)'} ${isPR && prNumber ? '(PR #' + prNumber + ')' : ''}</strong></div>
        <div><span style="color: #64748b; font-size: 6.5pt; font-weight: 700; display: block; text-transform: uppercase;">Gênero / Esperança</span><strong style="color: #0f172a;">${pub.gender || 'Masculino'} • ${pub.hope || 'Outras Ovelhas'}</strong></div>
        <div><span style="color: #64748b; font-size: 6.5pt; font-weight: 700; display: block; text-transform: uppercase;">Nascimento</span><strong style="color: #0f172a;">${formatDate(pub.birthDate)}</strong></div>
        <div><span style="color: #64748b; font-size: 6.5pt; font-weight: 700; display: block; text-transform: uppercase;">Batismo</span><strong style="color: #0f172a;">${formatDate(pub.baptismDate)}</strong></div>
      </div>

      <!-- Barra de Progresso do Pioneiro Regular -->
      ${pioneerSectionHtml}

      <!-- Tabela dos 12 Meses Teocráticos -->
      <table style="width: 100%; border-collapse: collapse; margin-bottom: 12px;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid #cbd5e1; font-size: 7.5pt; font-weight: 800; color: #334155; text-transform: uppercase; letter-spacing: 0.3px;">
            <th style="padding: 6px 8px; width: 28px; text-align: center;">Nº</th>
            <th style="padding: 6px 10px; text-align: left;">Mês Teocrático</th>
            <th style="padding: 6px 10px; width: 110px; text-align: center;">Trabalhou</th>
            <th style="padding: 6px 10px; width: 150px; text-align: left;">Privilégio no Mês</th>
            <th style="padding: 6px 10px; width: 65px; text-align: center;">Horas</th>
            <th style="padding: 6px 10px; width: 65px; text-align: center;">Estudos</th>
            <th style="padding: 6px 10px; text-align: left;">Observações</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>

      <!-- Resumo de Totais Anuais -->
      <div style="display: flex; justify-content: space-between; align-items: center; background: #eef2ff; border: 1.5px solid #c7d2fe; border-radius: 8px; padding: 8px 14px; font-size: 8.5pt; color: #1e1b4b;">
        <div>
          <span>Meses com Atividade: <strong style="font-size: 10pt; color: #4338ca;">${monthsWorkedCount} de 12</strong></span>
        </div>
        <div style="display: flex; gap: 20px;">
          <span>Total de Horas: <strong style="font-size: 10.5pt; color: #1e1b4b;">${totalHours} h</strong></span>
          <span>Média Mensal: <strong style="font-size: 10.5pt; color: #4338ca;">${avgHours} h/mês</strong></span>
          <span>Estudos Bíblicos: <strong style="font-size: 10.5pt; color: #4338ca;">${totalStudies}</strong></span>
        </div>
      </div>

      <!-- Rodapé -->
      <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 7pt; color: #94a3b8;">
        <span>Documento confidencial — Secretaria da Congregação</span>
        <span>Emitido em: ${new Date().toLocaleDateString('pt-BR')} às ${new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}</span>
      </div>
    </div>
  `;
}

function printPublisherCard(publisherName: string) {
  const pubInfo = publishers.value.find(p => p.name === publisherName) || {
    name: publisherName,
    group: '—',
    defaultPriv: 'PB',
    gender: 'Masculino',
    hope: 'Outras Ovelhas',
    active: true
  };
  const cardHtml = generateSinglePublisherCardHTML(pubInfo, false);

  const printWin = window.open('', '_blank');
  if (!printWin) return;

  printWin.document.write(`
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8">
      <title>Ficha de Publicador - ${publisherName}</title>
      <style>
        @page { size: A4 portrait; margin: 10mm 12mm; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 0; margin: 0; color: #0f172a; background: #fff; }
      </style>
    </head>
    <body>
      ${cardHtml}
      <script>window.onload = function() { window.print(); }<\/script>
    </body>
    </html>
  `);
  printWin.document.close();
}

function printAllPublishersCardsPDF() {
  const printWin = window.open('', '_blank');
  if (!printWin) return;

  const sortedPublishers = [...activePublishers.value].sort((a, b) => {
    if (a.group !== b.group) return a.group.localeCompare(b.group);
    return a.name.localeCompare(b.name, 'pt-BR');
  });

  const cardsHtml = sortedPublishers.map(pub => generateSinglePublisherCardHTML(pub, true)).join('');

  printWin.document.write(`
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8">
      <title>Fichas Individuais de Atividades — Todos os Publicadores</title>
      <style>
        @page { size: A4 portrait; margin: 10mm 12mm; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; margin: 0; padding: 0; background: #ffffff; }
      </style>
    </head>
    <body>
      ${cardsHtml}
      <script>window.onload = function() { window.print(); }<\/script>
    </body>
    </html>
  `);
  printWin.document.close();
}

function triggerPrint() {
  const currentM = selectedMonth.value === 'all' ? 'Todos os Meses' : selectedMonth.value;
  const currentY = selectedServiceYear.value;
  const printWin = window.open('', '_blank');
  if (!printWin) return;

  const rows = filteredReports.value.map((r, i) => `
    <tr style="border-bottom: 1px solid #e2e8f0; font-size: 8.5pt;">
      <td style="padding: 6px; text-align: center; color: #64748b;">${i + 1}</td>
      <td style="padding: 6px 10px; font-weight: 700; color: #0f172a;">${r.name}</td>
      <td style="padding: 6px; text-align: center;"><span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 7.5pt; font-weight: 600;">${r.group}</span></td>
      <td style="padding: 6px; text-align: center; color: #475569;">${r.month} (${r.service_year})</td>
      <td style="padding: 6px 10px; color: #334155;">${r.privilege}</td>
      <td style="padding: 6px; text-align: center; font-weight: 800; color: #1e1b4b;">${r.hours} h</td>
      <td style="padding: 6px; text-align: center; font-weight: 700; color: #4338ca;">${r.estudos}</td>
      <td style="padding: 6px; text-align: center;"><span style="background: #dcfce7; color: #15803d; font-weight: 700; padding: 2px 6px; border-radius: 4px; font-size: 7pt;">${r.worked || 'Sim'}</span></td>
      <td style="padding: 6px 10px; color: #64748b; font-style: italic; font-size: 8pt;">${r.obs || '—'}</td>
    </tr>
  `).join('');

  printWin.document.write(`
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8">
      <title>Relatórios Entregues — ${currentM} (${currentY})</title>
      <style>
        @page { size: A4 portrait; margin: 10mm 12mm; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; margin: 0; padding: 0; background: #fff; }
      </style>
    </head>
    <body>
      <div style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2.5px solid #4f46e5; padding-bottom: 8px; margin-bottom: 12px;">
        <div>
          <h1 style="margin: 0; font-size: 16pt; font-weight: 800; color: #0f172a;">Relação Analítica de Relatórios Entregues</h1>
          <p style="margin: 3px 0 0 0; font-size: 8.5pt; color: #64748b;">Mês: <strong>${currentM}</strong> • Ano Teocrático: <strong>${currentY}</strong> • Total: <strong>${filteredReports.value.length} entregues</strong></p>
        </div>
        <div style="text-align: right; font-size: 7.5pt; color: #64748b;">
          <div>Secretaria da Congregação</div>
          <div>Emitido em: ${new Date().toLocaleDateString('pt-BR')} às ${new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}</div>
        </div>
      </div>

      <!-- Resumo rápido -->
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 14px;">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 10px; text-align: center;">
          <span style="font-size: 6.5pt; font-weight: 700; color: #64748b; text-transform: uppercase; display: block;">Total de Horas</span>
          <span style="font-size: 13pt; font-weight: 800; color: #0f172a;">${stats.value.totalHours} h</span>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 10px; text-align: center;">
          <span style="font-size: 6.5pt; font-weight: 700; color: #64748b; text-transform: uppercase; display: block;">Média de Horas</span>
          <span style="font-size: 13pt; font-weight: 800; color: #4338ca;">${stats.value.avgHours} h</span>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 10px; text-align: center;">
          <span style="font-size: 6.5pt; font-weight: 700; color: #64748b; text-transform: uppercase; display: block;">No Campo</span>
          <span style="font-size: 13pt; font-weight: 800; color: #15803d;">${stats.value.worked}</span>
        </div>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 10px; text-align: center;">
          <span style="font-size: 6.5pt; font-weight: 700; color: #64748b; text-transform: uppercase; display: block;">Estudos Bíblicos</span>
          <span style="font-size: 13pt; font-weight: 800; color: #4338ca;">${stats.value.studies}</span>
        </div>
      </div>

      <table style="width: 100%; border-collapse: collapse;">
        <thead>
          <tr style="background: #f1f5f9; border-bottom: 2px solid #cbd5e1; font-size: 7.5pt; font-weight: 800; color: #334155; text-transform: uppercase;">
            <th style="padding: 6px; width: 28px; text-align: center;">#</th>
            <th style="padding: 6px 10px; text-align: left;">Publicador</th>
            <th style="padding: 6px; width: 75px; text-align: center;">Grupo</th>
            <th style="padding: 6px; width: 100px; text-align: center;">Mês/Ano</th>
            <th style="padding: 6px 10px; width: 140px; text-align: left;">Privilégio</th>
            <th style="padding: 6px; width: 55px; text-align: center;">Horas</th>
            <th style="padding: 6px; width: 55px; text-align: center;">Estudos</th>
            <th style="padding: 6px; width: 70px; text-align: center;">Trabalhou</th>
            <th style="padding: 6px 10px; text-align: left;">Observações</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>

      <div style="margin-top: 14px; padding-top: 8px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 7.5pt; color: #94a3b8;">
        <span>Gestão de Relatórios — Congregação</span>
        <span>Total listado: ${filteredReports.value.length} irmãos</span>
      </div>

      <script>window.onload = function() { window.print(); }<' + '/script>
    </body>
    </html>
  `);
  printWin.document.close();
}

function printPendingListPDF() {
  const m = selectedMonth.value === 'all' ? 'Outubro' : selectedMonth.value;
  const yr = selectedServiceYear.value === 'all' ? '2026/2027' : selectedServiceYear.value;
  const printWin = window.open('', '_blank');
  if (!printWin) return;

  const nowStr = new Date().toLocaleDateString('pt-BR') + ' às ' + new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  const totalPend = pendingPublishers.value.length;
  const totalActive = activePublishers.value.length;
  const totalEntregues = totalActive - totalPend;
  const percEntregue = totalActive > 0 ? ((totalEntregues / totalActive) * 100).toFixed(1) : '0.0';

  let groupsHtml = '';
  groupNames.value.forEach(g => {
    const pendList = groupPending(g);
    const isComplete = pendList.length === 0;

    let itemsHtml = '';
    if (isComplete) {
      itemsHtml = `
        <div style="text-align: center; padding: 18px 8px; color: #15803d;">
          <div style="font-size: 16pt; line-height: 1;">✓</div>
          <div style="font-weight: 700; font-size: 8.5pt; margin-top: 4px;">100% Entregue</div>
          <div style="font-size: 7.5pt; color: #16a34a;">Nenhum relatório pendente</div>
        </div>
      `;
    } else {
      itemsHtml = '<ol style="margin: 0; padding-left: 18px; font-size: 8pt; line-height: 1.5; color: #1e293b;">';
      pendList.forEach(p => {
        itemsHtml += `<li style="padding: 1.5px 0; border-bottom: 1px dotted #f1f5f9;"><strong>${p.name}</strong> <span style="font-size: 7pt; color: #64748b;">(${p.defaultPriv || 'PB'})</span></li>`;
      });
      itemsHtml += '</ol>';
    }

    groupsHtml += `
      <div style="border: 1.5px solid ${isComplete ? '#86efac' : '#fca5a5'}; border-radius: 8px; background: ${isComplete ? '#f0fdf4' : '#ffffff'}; padding: 10px 12px; break-inside: avoid; margin-bottom: 10px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid ${isComplete ? '#bbf7d0' : '#fee2e2'}; padding-bottom: 6px; margin-bottom: 8px;">
          <span style="font-weight: 800; font-size: 9.5pt; color: #0f172a; text-transform: uppercase;">${g}</span>
          <span style="font-size: 7.5pt; font-weight: 700; padding: 2px 8px; border-radius: 12px; background: ${isComplete ? '#dcfce7' : '#fee2e2'}; color: ${isComplete ? '#166534' : '#991b1b'};">
            ${isComplete ? '100% Concluído' : pendList.length + ' pendentes'}
          </span>
        </div>
        ${itemsHtml}
      </div>
    `;
  });

  printWin.document.write(`
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8">
      <title>Relatórios Pendentes — ${m} (${yr})</title>
      <style>
        @page { size: A4 portrait; margin: 10mm 12mm; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #0f172a; margin: 0; padding: 0; background: #ffffff; }
      </style>
    </head>
    <body>
      <div style="display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2.5px solid #d97706; padding-bottom: 8px; margin-bottom: 10px;">
        <div>
          <h1 style="margin: 0; font-size: 15pt; color: #1e293b; font-weight: 800; letter-spacing: -0.5px;">Controle de Cobrança de Relatórios</h1>
          <p style="margin: 2px 0 0 0; font-size: 8.5pt; color: #64748b;">Mês de Referência: <strong>${m}</strong> • Ano Teocrático: <strong>${yr}</strong></p>
        </div>
        <div style="text-align: right; font-size: 7.5pt; color: #64748b;">
          <div>Emitido em: <strong>${nowStr}</strong></div>
          <div style="color: #b45309; font-weight: 600;">Secretaria da Congregação</div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px;">
        <div style="border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 8px; text-align: center; background: #f8fafc;">
          <span style="font-size: 6.5pt; font-weight: 700; text-transform: uppercase; color: #64748b; display: block;">Publicadores Ativos</span>
          <span style="font-size: 13pt; font-weight: 800; margin-top: 1px; display: block; color: #334155;">${totalActive}</span>
        </div>
        <div style="border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 8px; text-align: center; background: #f8fafc;">
          <span style="font-size: 6.5pt; font-weight: 700; text-transform: uppercase; color: #64748b; display: block;">Relatórios Entregues</span>
          <span style="font-size: 13pt; font-weight: 800; margin-top: 1px; display: block; color: #15803d;">${totalEntregues}</span>
        </div>
        <div style="border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 8px; text-align: center; background: #f8fafc;">
          <span style="font-size: 6.5pt; font-weight: 700; text-transform: uppercase; color: #64748b; display: block;">Faltam Entregar</span>
          <span style="font-size: 13pt; font-weight: 800; margin-top: 1px; display: block; color: #b91c1c;">${totalPend}</span>
        </div>
        <div style="border: 1px solid #e2e8f0; border-radius: 6px; padding: 6px 8px; text-align: center; background: #f8fafc;">
          <span style="font-size: 6.5pt; font-weight: 700; text-transform: uppercase; color: #64748b; display: block;">Progresso Geral</span>
          <span style="font-size: 13pt; font-weight: 800; margin-top: 1px; display: block; color: #4f46e5;">${percEntregue}%</span>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">
        ${groupsHtml}
      </div>

      <div style="margin-top: 14px; padding-top: 8px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; font-size: 7.5pt; color: #64748b;">
        <span>Gestão de Relatórios e Grupos — Congregação</span>
        <span>Documento para acompanhamento exclusivo dos dirigentes de grupo</span>
      </div>

      <script>window.onload = function() { window.print(); }<' + '/script>
    </body>
    </html>
  `);
  printWin.document.close();
}

function copyWhatsAppPendingText() {
  const m = selectedMonth.value === 'all' ? 'Outubro' : selectedMonth.value;
  let text = `📢 *RELATÓRIOS PENDENTES — ${m.toUpperCase()}*\n`;
  text += `Total de pendências: ${pendingPublishers.value.length}\n\n`;

  groupNames.value.forEach(g => {
    const pend = groupPending(g);
    text += `*${g.toUpperCase()}* (${pend.length === 0 ? '100% Entregue ✅' : pend.length + ' faltam'}):\n`;
    if (pend.length === 0) {
      text += `  • Nenhum pendente!\n`;
    } else {
      pend.forEach(p => {
        text += `  • ${p.name}\n`;
      });
    }
    text += `\n`;
  });

  navigator.clipboard.writeText(text);
}

onMounted(async () => {
  applyTheme(isDark.value);

  // 1. Tenta carregar do banco de dados PostgreSQL
  dbConnected.value = await api.checkHealth();
  if (dbConnected.value) {
    try {
      const [dbGroups, dbPubs, dbReps] = await Promise.all([
        api.getGroups(),
        api.getPublishers(),
        api.getReports()
      ]);

      if (dbGroups?.length) groups.value = dbGroups;
      if (dbPubs?.length) publishers.value = dbPubs;
      if (dbReps?.length) reports.value = dbReps;
    } catch (e) {
      console.warn("Falha na sincronização inicial do banco, usando cache local:", e);
    }
  } else {
    // 2. Fallback para localStorage
    const sGroups = localStorage.getItem('gestao_grupos_data');
    if (sGroups) groups.value = JSON.parse(sGroups);
    const sPubs = localStorage.getItem('gestao_publicadores_data');
    if (sPubs) publishers.value = JSON.parse(sPubs);
    const sReps = localStorage.getItem('gestao_relatorios_data');
    if (sReps) reports.value = JSON.parse(sReps);
  }
});
</script>