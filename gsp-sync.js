(function (scope) {
  'use strict';
  const clone = value => JSON.parse(JSON.stringify(value));
  // O Firebase pode devolver arrays como objetos e remove nós vazios.
  function canonical(value) {
    if (value === null || value === undefined) return null;
    if (typeof value !== 'object') return value;
    const result = {};
    Object.keys(value).sort().forEach(key => {
      const child = canonical(value[key]);
      if (child !== null) result[key] = child;
    });
    return Object.keys(result).length ? result : null;
  }
  const fingerprint = value => JSON.stringify(canonical(value));
  class GspSync {
    constructor(ref, isAuthorized) {
      this.ref = ref;
      this.isAuthorized = isAuthorized;
      this.loaded = false;
      this.saving = false;
      this.baseline = null;
    }
    async load() {
      this.loaded = false;
      if (!this.isAuthorized()) throw new Error('Acesso não autorizado.');
      const snapshot = await this.ref.once('value');
      if (!this.isAuthorized()) throw new Error('A sessão foi encerrada.');
      this.baseline = snapshot.val();
      this.loaded = true;
      return clone(this.baseline || {});
    }
    async save(clients, options) {
      if (!this.loaded || !this.isAuthorized()) throw new Error('Entre e carregue os dados antes de salvar.');
      if (this.saving) throw new Error('Já existe um salvamento em andamento.');
      this.saving = true;
      const expected = fingerprint(this.baseline);
      const next = clone({ ...(this.baseline || {}), clients, options: { ...(this.baseline?.options || {}), ...options } });
      const keepCache = () => {};
      try {
        // Mantém a leitura no cache durante a transação. Nunca aceita um
        // primeiro valor null como se fosse prova de que o servidor está vazio.
        this.ref.on('value', keepCache, () => {});
        await this.ref.once('value');
        // Aborta se outra aba/dispositivo modificou qualquer dado desde a leitura.
        // applyLocally=false evita mostrar uma gravação ainda não confirmada.
        const result = await this.ref.transaction(current => {
          if (!this.isAuthorized() || fingerprint(current) !== expected) return;
          return next;
        }, undefined, false);
        if (!result.committed) {
          this.loaded = false;
          throw new Error('Os dados mudaram em outra aba ou dispositivo. Baixe a tentativa não salva e recarregue a nuvem antes de refazer a alteração.');
        }
        this.baseline = result.snapshot.val();
        return clone(this.baseline || {});
      } finally {
        this.ref.off('value', keepCache);
        this.saving = false;
      }
    }
  }
  scope.GspSync = GspSync;
})(typeof window === 'undefined' ? globalThis : window);
