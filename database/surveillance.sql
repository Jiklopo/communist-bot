CREATE TABLE IF NOT EXISTS surveillance(
    watcher_id bigint NOT NULL,
    target_id bigint NOT NULL,
    start_date date NOT NULL DEFAULT current_date,
    FOREIGN KEY (watcher_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT cannot_watch_yourself CHECK ( watcher_id != target_id ),
    CONSTRAINT unique_combos UNIQUE (watcher_id, target_id)
);