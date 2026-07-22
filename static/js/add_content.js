// ========== ФУНКЦИИ ДЛЯ РАБОТЫ С ОКНОМ КОДОВ ==========

// Открыть окно и обновить список
function openFillCodesModal() {
    updateCodesListDisplay();
    $('#fillCodesModal').modal('show');
    // Автофокус на поле ввода
    setTimeout(() => {
        document.getElementById('codeInput').focus();
    }, 500);
}

// Обновить отображение списка кодов
function updateCodesListDisplay() {
    let codes = localStorage.getItem('my_codes');
    if (codes) {
        codes = JSON.parse(codes);
    } else {
        codes = [];
    }

    // Обновляем счетчик
    document.getElementById('codesCount').textContent = codes.length;

    // Обновляем список
    const container = document.getElementById('codesListContainer');
    if (codes.length === 0) {
        container.innerHTML = '<div class="text-muted text-center p-3">Нет добавленных кодов</div>';
        return;
    }

    let html = '<div class="list-group list-group-flush">';
    codes.forEach((code, index) => {
        // Обрезаем длинные коды для отображения
        const displayCode = code.length > 80 ? code.substring(0, 37) + '...' : code;
        html += `
            <div class="list-group-item d-flex justify-content-between align-items-center" style="">
                <code class="small" style="word-break: break-all; flex: 1;">${escapeHtml(displayCode)}</code>
                <button class="btn btn-sm btn-danger ms-2" onclick="removeCodeFromListModal(${index})" title="Удалить">
                    ✕
                </button>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}

// Удалить код из списка по индексу
function removeCodeFromListModal(index) {
    let codes = localStorage.getItem('my_codes');
    if (codes) {
        codes = JSON.parse(codes);
        codes.splice(index, 1);
        localStorage.setItem('my_codes', JSON.stringify(codes));
        updateCodesListDisplay();
    }
}

// Очистить все коды
function clearAllCodesModal() {
    if (confirm('Вы уверены, что хотите удалить ВСЕ коды?')) {
        localStorage.removeItem('my_codes');
        updateCodesListDisplay();
        console.log('Все коды удалены');
    }
}

// Экспорт в JSON файл
function exportCodesToFileModal() {
    let codes = localStorage.getItem('my_codes');
    if (!codes || JSON.parse(codes).length === 0) {
        alert('Нет кодов для экспорта');
        return;
    }

    codes = JSON.parse(codes);
    const dataStr = JSON.stringify(codes, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    const exportFileDefaultName = `codes_${new Date().toISOString().slice(0,19).replace(/:/g, '-')}.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();

    alert(`Экспортировано ${codes.length} кодов`);
}

// Копировать все коды в буфер обмена
function copyCodesToClipboard() {
    let codes = localStorage.getItem('my_codes');
    if (!codes || JSON.parse(codes).length === 0) {
        alert('Нет кодов для копирования');
        return;
    }

    codes = JSON.parse(codes);
    const text = codes.join('\n');

    navigator.clipboard.writeText(text).then(() => {
        alert(`Скопировано ${codes.length} кодов в буфер обмена`);
    }).catch(() => {
        alert('Ошибка копирования');
    });
}

// Экранирование HTML специальных символов
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========== ОБРАБОТЧИК ВВОДА КОДА ==========

function AddContent() {
    alert('Ввод активирован')
    const codeInput = document.getElementById('codeInput');
    if (codeInput) {
        let timeout = null;

        // Основной обработчик ввода
        const processInput = function() {
            const code = codeInput.value.trim();
            if (code) {
                saveCodeToLocalStorage(code);
                updateCodesListDisplay();
                codeInput.value = '';
            }
        };

        // Несколько событий для мобильной поддержки
        codeInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter' || event.keyCode === 13) {
                processInput();
            }
        });

        // Событие input для мобильных устройств
        codeInput.addEventListener('input', function(event) {
            // Можно добавить debounce для автоматического сохранения
            if (timeout) clearTimeout(timeout);
            timeout = setTimeout(processInput, 500);
        });

        // Для кнопки "Готово" на мобильной клавиатуре
        codeInput.addEventListener('blur', function() {
            if (codeInput.value.trim()) {
                processInput();
            }
        });
    }
}

// Сохранение кода с проверкой на дубликаты
function saveCodeToLocalStorage(code) {
    if (!code) return;

    let codes = localStorage.getItem('my_codes');
    if (codes) {
        codes = JSON.parse(codes);
    } else {
        codes = [];
    }

    // Проверка на дубликат
    if (codes.includes(code)) {
        showTempMessage('⚠️ Код уже существует: ' + code.substring(0, 20) + '...', 'warning');
        return;
    }

    codes.push(code);
    localStorage.setItem('my_codes', JSON.stringify(codes));

    console.log('Код сохранен:', code);
    console.log('Всего кодов:', codes.length);

    showTempMessage('✅ Код добавлен! Всего: ' + codes.length, 'success');
}

// Временное сообщение
function showTempMessage(message, type) {
    const container = document.getElementById('codesListContainer');
    if (!container) return;

    const oldAlert = document.querySelector('.temp-alert');
    if (oldAlert) oldAlert.remove();

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'warning'} alert-dismissible fade show temp-alert`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    container.parentNode.insertBefore(alertDiv, container);

    setTimeout(() => {
        if (alertDiv) alertDiv.remove();
    }, 2000);
}