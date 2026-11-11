// src/services/api.ts
// Comunicação com a API do banco de dados (PostgreSQL local ou backend)

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface Group {
    id?: number;
    name: string;
    overseer?: string;       // Dirigente
    assistant?: string;      // Ajudante
    meeting_place?: string;  // Ponto de encontro da saída
    active?: boolean;
}

export interface Publisher {
    id?: string;
    name: string;
    group_id?: number;
    group: string;
    defaultPriv: string;
    gender: string;
    birthDate?: string;
    baptismDate?: string;
    hope: string;
    active: boolean;
    obs?: string;
}

export interface Report {
    id?: number | string;
    name: string;
    group_id?: number;
    group: string;
    month: string;
    service_year: string;
    privilege: string;
    hours: number;
    revisitas: number;
    estudos: number;
    worked: string;
    obs?: string;
}

export const api = {
    // Teste de conexão
    async checkHealth(): Promise<boolean> {
        try {
            const res = await fetch(`${API_BASE_URL}/health`, { method: 'GET' });
            return res.ok;
        } catch {
            return false;
        }
    },

    // Grupos
    async getGroups(): Promise<Group[]> {
        const res = await fetch(`${API_BASE_URL}/groups`);
        if (!res.ok) throw new Error('Falha ao carregar grupos');
        return res.json();
    },

    async saveGroup(group: Group): Promise<{ status: string; id: number; name: string }> {
        const res = await fetch(`${API_BASE_URL}/groups`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(group)
        });
        if (!res.ok) throw new Error('Falha ao salvar grupo');
        return res.json();
    },

    // Publicadores
    async getPublishers(): Promise<Publisher[]> {
        const res = await fetch(`${API_BASE_URL}/publishers`);
        if (!res.ok) throw new Error('Falha ao carregar publicadores');
        return res.json();
    },

    async savePublisher(pub: Publisher): Promise<Publisher> {
        const res = await fetch(`${API_BASE_URL}/publishers`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(pub)
        });
        if (!res.ok) throw new Error('Falha ao salvar publicador');
        return res.json();
    },

    // Relatórios
    async getReports(month?: string, service_year?: string): Promise<Report[]> {
        const params = new URLSearchParams();
        if (month && month !== 'all') params.append('month', month);
        if (service_year && service_year !== 'all') params.append('service_year', service_year);

        const res = await fetch(`${API_BASE_URL}/reports?${params.toString()}`);
        if (!res.ok) throw new Error('Falha ao carregar relatórios');
        return res.json();
    },

    async saveReport(report: Report): Promise<{ status: string; id?: number }> {
        const res = await fetch(`${API_BASE_URL}/reports`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(report)
        });
        if (!res.ok) throw new Error('Falha ao salvar relatório');
        return res.json();
    },

    async deleteReport(id: number | string): Promise<void> {
        await fetch(`${API_BASE_URL}/reports/${id}`, { method: 'DELETE' });
    }
};