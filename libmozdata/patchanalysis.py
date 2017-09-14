def reviewer_match(short_name, bugzilla_reviewers, cc_list, reviewer_cache={}):
            warnings.warn('Reviewer ' + reviewer_cache[short_name] + ' is not in the list of reviewers on Bugzilla (' + ', '.join(sorted(bugzilla_reviewers)) + ').', stacklevel=3)
            warnings.warn('Reviewer ' + elem + ' is not in the list of reviewers on Bugzilla (' + ', '.join(sorted(bugzilla_reviewers)) + ').', stacklevel=3)
def author_match(author_mercurial, author_real_name, bugzilla_authors, cc_list, author_cache={}):
    if author_mercurial in author_cache:
        if not any(a in bugzilla_authors for a in author_cache[author_mercurial]):
            warnings.warn('None of ' + ', '.join(sorted(author_cache[author_mercurial])) + ' is in the list of authors on Bugzilla (' + ', '.join(sorted(bugzilla_authors)) + ').', stacklevel=3)

        return set([author_mercurial] + author_cache[author_mercurial])

        assert author_mercurial not in author_cache
        author_cache[author_mercurial] = [author_mercurial]
            warnings.warn('Author ' + elem + ' is not in the list of authors on Bugzilla (' + ', '.join(sorted(bugzilla_authors)) + ').', stacklevel=3)
            assert author_mercurial not in author_cache
            author_cache[author_mercurial] = [author_mercurial]
    assert author_mercurial not in author_cache
    result = set([author_mercurial, found.pop()])
    author_cache[author_mercurial] = list(result)
    return result
        if diff.changes is None:
            assert any(subtext in diff.text for subtext in ['new mode ', 'rename ', 'copy ', 'new file mode ', 'deleted file mode ']) or any(subtext1 in diff.text and subtext2 in diff.text for (subtext1, subtext2) in [('Binary file ', ' has changed')]), 'Can\'t parse changes from patch: ' + str(diff)
            # Calc changes additions & deletions
            counts = [(
                old is None and new is not None,
                new is None and old is not None
            ) for old, new, _ in diff.changes]
            counts = list(zip(*counts))  # inverse zip
            info['changes_add'] += sum(counts[0])
            info['changes_del'] += sum(counts[1])

            # TODO: Split C/C++, Rust, Java, JavaScript, build system changes
            if _is_test(new_path):
                info['test_changes_size'] += len(diff.changes)
            else:
                info['changes_size'] += len(diff.changes)
            if flag['name'] != 'review' or flag['status'] == '-':
                continue

    reviewer_pattern = re.compile('r=([a-zA-Z0-9._]+)')
def bug_analysis(bug, uplift_channel=None, author_cache={}, reviewer_cache={}):
            author_names = author_match(obj['author_mercurial'], obj['author_real_name'], bugzilla_authors, bug['cc_detail'], author_cache)
                    reviewers.add(reviewer_match(short_reviewer, bugzilla_reviewers | bugzilla_authors, bug['cc_detail'], reviewer_cache))
                info['patches'][attachment['id']].update(patch_analysis(data, [attachment['creator']], bugzilla_reviewers, utils.get_date_ymd(attachment['creation_time'])))
    if uplift_channel is not None:
        # Add uplift request
        info.update(uplift_info(bug, uplift_channel))
        # Sometimes a patch is approved for uplift without a request.
        # assert info['response_delta'] >= timedelta(), "Delta between uplift request date and response should be at least 0"
        assert info['release_delta'] > timedelta(), "Delta between uplift request date and next release should be at least 0"